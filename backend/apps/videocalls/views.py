from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from livekit.api import AccessToken, VideoGrants
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsAdmin, IsStudent

from .models import VideoCall


def _mint_token(room_name: str, identity: str, name: str) -> str:
    grants = VideoGrants(room_join=True, room=room_name, can_publish=True, can_subscribe=True)
    return (
        AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(identity)
        .with_name(name)
        .with_grants(grants)
        .to_jwt()
    )


def _serialize_call(call: VideoCall, *, identity: str, name: str) -> dict:
    return {
        'callId': call.id,
        'roomName': call.room_name,
        'livekitUrl': settings.LIVEKIT_URL,
        'token': _mint_token(call.room_name, identity, name),
    }


class StartCallView(APIView):
    """POST /api/videocalls/start/ {student_id} — admin starts a call, mirrors
    apps.reviews.views.SubmitReviewView's shape (IsAdmin, get_object_or_404)."""

    permission_classes = [IsAdmin]

    def post(self, request):
        student = get_object_or_404(User, id=request.data.get('student_id'), role=User.Role.STUDENT)
        call = VideoCall.objects.create(student=student, initiator=request.user)
        identity = f'admin-{request.user.id}'
        name = request.user.get_full_name() or request.user.email
        return Response(_serialize_call(call, identity=identity, name=name))


class ActiveCallView(APIView):
    """GET /api/videocalls/active/ — polled by the student frontend (no
    WebSockets in this stack) to detect an incoming call."""

    permission_classes = [IsStudent]

    def get(self, request):
        call = (
            VideoCall.objects.filter(student=request.user, status__in=[VideoCall.Status.PENDING, VideoCall.Status.ACTIVE])
            .order_by('-created_at')
            .first()
        )
        if not call:
            return Response(None)
        initiator = call.initiator
        return Response({
            'callId': call.id,
            'status': call.status,
            'initiatorName': (initiator.get_full_name() or initiator.email) if initiator else '',
        })


class JoinCallView(APIView):
    """POST /api/videocalls/<id>/join/ — mints a token for whichever
    participant (student or initiating admin) is joining."""

    permission_classes = [IsAuthenticated]

    def post(self, request, call_id):
        call = get_object_or_404(VideoCall, id=call_id)
        user = request.user
        if call.student_id != user.id and call.initiator_id != user.id:
            return Response({'detail': 'Not a participant of this call.'}, status=403)

        if call.status == VideoCall.Status.PENDING:
            call.status = VideoCall.Status.ACTIVE
            call.save(update_fields=['status'])

        is_student = call.student_id == user.id
        identity = f'student-{user.id}' if is_student else f'admin-{user.id}'
        name = user.get_full_name() or user.email
        return Response(_serialize_call(call, identity=identity, name=name))


class EndCallView(APIView):
    """POST /api/videocalls/<id>/end/ — either participant can end the call."""

    permission_classes = [IsAuthenticated]

    def post(self, request, call_id):
        call = get_object_or_404(VideoCall, id=call_id)
        user = request.user
        if call.student_id != user.id and call.initiator_id != user.id:
            return Response({'detail': 'Not a participant of this call.'}, status=403)

        call.status = VideoCall.Status.ENDED
        call.ended_at = timezone.now()
        call.save(update_fields=['status', 'ended_at'])
        return Response({'ended': True})
