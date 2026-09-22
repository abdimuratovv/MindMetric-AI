"""
Written student-admin support channel - the counterpart to apps.videocalls.

Role split, mirroring the rest of the project: a student only ever sees their
own threads (the queryset is scoped by `student=request.user`, so a guessed id
404s instead of leaking someone else's report), while any admin can open any
thread from the inbox. Reads/writes are plain REST - the frontend refreshes on
navigation, and the polling/unread badge lands in a later phase, the same way
apps.videocalls settled on short polling rather than WebSockets.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.permissions import IsAdmin, IsStudent
from apps.i18n import get_language

from .labels import category_options, status_options
from .models import SupportMessage, SupportThread
from .serializers import (
    ERRORS,
    error,
    serialize_message,
    serialize_thread_detail,
    serialize_thread_row,
    validate_message_body,
    validate_thread_payload,
)

# The inbox/my-threads lists are unpaginated but bounded - admins narrow the
# queue with the status/category/assignee filters instead of paging through it,
# and a student cannot realistically own more than a handful (see the throttle).
THREAD_LIST_LIMIT = 100


class _StudentThrottle(ScopedRateThrottle):
    """Rate-limits students only; an admin working through the inbox is never
    throttled. Guards against a frustrated student (or a script) flooding the
    queue - there is no email/notification infra to absorb that."""

    def allow_request(self, request, view):
        user = request.user
        if user.is_authenticated and user.role == User.Role.ADMIN:
            return True
        return super().allow_request(request, view)


def _thread_for(user, thread_id) -> SupportThread:
    qs = SupportThread.objects.select_related('student', 'assignee')
    if user.role == User.Role.ADMIN:
        return get_object_or_404(qs, id=thread_id)
    return get_object_or_404(qs, id=thread_id, student=user)


def _append_message(thread: SupportThread, author, body: str) -> SupportMessage:
    """Creates the message and moves the thread's queue state with it - the
    single place where status/unread/last_message_at are kept consistent."""
    message = SupportMessage.objects.create(thread=thread, author=author, body=body)
    thread.last_message_at = message.created_at
    if author.role == User.Role.ADMIN:
        thread.status = SupportThread.Status.ANSWERED
        thread.student_unread += 1
        thread.admin_unread = 0
        # First admin to answer an unassigned ("any admin") thread takes it,
        # so the shared queue does not get worked twice.
        if thread.assignee_id is None:
            thread.assignee = author
    else:
        # A reply on a resolved thread reopens it - otherwise a student's
        # follow-up would sit in a closed thread nobody looks at again.
        thread.status = SupportThread.Status.OPEN
        thread.admin_unread += 1
        thread.student_unread = 0
    thread.save()
    return message


def _mark_read(thread: SupportThread, viewer) -> None:
    field = 'admin_unread' if viewer.role == User.Role.ADMIN else 'student_unread'
    if getattr(thread, field):
        setattr(thread, field, 0)
        thread.save(update_fields=[field])


class SupportOptionsView(APIView):
    """
    GET /api/support/options/

    Everything the composer and the inbox filters need in one round trip:
    the ru/uz category and status vocabularies (translated server-side, see
    apps.support.labels) plus the admins a student can address a thread to.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        lang = get_language(request)
        admins = User.objects.filter(role=User.Role.ADMIN).order_by('first_name', 'last_name', 'email')
        return Response({
            'categories': category_options(lang),
            'statuses': status_options(lang),
            'admins': [
                {'id': a.id, 'name': a.get_full_name() or a.email, 'initials': a.initials}
                for a in admins
            ],
        })


class ThreadListCreateView(APIView):
    """
    GET  /api/support/threads/ - the student's own threads, or the admin inbox
         filtered by ?status=&category=&assignee=me|unassigned|all&search=
    POST /api/support/threads/ {category, subject, body, assignee_id?} - a
         student opens a new report; `assignee_id` omitted means "any admin".
    """

    def get_permissions(self):
        return [IsStudent()] if self.request.method == 'POST' else [IsAuthenticated()]

    def get_throttles(self):
        if self.request.method == 'POST':
            self.throttle_scope = 'support-thread'
            return [_StudentThrottle()]
        return []

    def throttled(self, request, wait):
        exc = super().throttled(request, wait)
        exc.detail = ERRORS['too_many_threads'][get_language(request)]
        raise exc

    def get(self, request):
        lang = get_language(request)
        user = request.user
        threads = SupportThread.objects.select_related('student', 'assignee')

        if user.role == User.Role.ADMIN:
            assignee = request.query_params.get('assignee', 'all')
            if assignee == 'me':
                threads = threads.filter(assignee=user)
            elif assignee == 'unassigned':
                threads = threads.filter(assignee__isnull=True)

            status_filter = request.query_params.get('status', '')
            if status_filter in SupportThread.Status.values:
                threads = threads.filter(status=status_filter)

            category = request.query_params.get('category', '')
            if category in SupportThread.Category.values:
                threads = threads.filter(category=category)

            search = request.query_params.get('search', '')
            if search:
                threads = threads.filter(
                    Q(subject__icontains=search)
                    | Q(student__first_name__icontains=search)
                    | Q(student__last_name__icontains=search)
                )
        else:
            threads = threads.filter(student=user)

        threads = list(threads.order_by('-last_message_at')[:THREAD_LIST_LIMIT])

        # One query for the whole page's previews instead of one per row.
        last_by_thread = {}
        for message in SupportMessage.objects.filter(thread__in=threads).order_by('id'):
            last_by_thread[message.thread_id] = message

        return Response([
            serialize_thread_row(t, lang, user, last_message=last_by_thread.get(t.id))
            for t in threads
        ])

    def post(self, request):
        lang = get_language(request)
        cleaned, err = validate_thread_payload(request.data, lang)
        if err:
            return Response(err, status=400)

        thread = SupportThread.objects.create(
            student=request.user,
            assignee=cleaned['assignee'],
            category=cleaned['category'],
            subject=cleaned['subject'],
        )
        message = _append_message(thread, request.user, cleaned['body'])
        return Response(serialize_thread_detail(thread, lang, request.user, [message]), status=201)


class ThreadDetailView(APIView):
    """
    GET   /api/support/threads/{id}/ - thread + full message history; clears the
          caller's unread counter.
    PATCH /api/support/threads/{id}/ {status?, assignee_id?} - admin-only queue
          management (resolve/reopen, take over or hand off a thread).
    """

    def get_permissions(self):
        return [IsAdmin()] if self.request.method == 'PATCH' else [IsAuthenticated()]

    def get(self, request, thread_id):
        lang = get_language(request)
        thread = _thread_for(request.user, thread_id)
        messages = list(thread.messages.select_related('author'))
        _mark_read(thread, request.user)
        return Response(serialize_thread_detail(thread, lang, request.user, messages))

    def patch(self, request, thread_id):
        lang = get_language(request)
        thread = _thread_for(request.user, thread_id)

        if 'status' in request.data:
            status_value = request.data.get('status')
            if status_value not in SupportThread.Status.values:
                return Response(error('invalid_status', lang), status=400)
            thread.status = status_value

        if 'assignee_id' in request.data:
            raw = request.data.get('assignee_id')
            if raw in (None, '', 0, '0'):
                thread.assignee = None
            else:
                admin = User.objects.filter(id=raw, role=User.Role.ADMIN).first()
                if admin is None:
                    return Response(error('invalid_assignee', lang), status=400)
                thread.assignee = admin

        thread.save()
        messages = list(thread.messages.select_related('author'))
        return Response(serialize_thread_detail(thread, lang, request.user, messages))


class ThreadMessagesView(APIView):
    """
    GET  /api/support/threads/{id}/messages/?after={id} - messages newer than
         `after`, so an open conversation can refresh without refetching it all.
    POST /api/support/threads/{id}/messages/ {body} - reply, from either side.
    """

    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == 'POST':
            self.throttle_scope = 'support-message'
            return [_StudentThrottle()]
        return []

    def throttled(self, request, wait):
        exc = super().throttled(request, wait)
        exc.detail = ERRORS['too_many_messages'][get_language(request)]
        raise exc

    def get(self, request, thread_id):
        thread = _thread_for(request.user, thread_id)
        messages = thread.messages.select_related('author')
        after = request.query_params.get('after')
        if after and after.isdigit():
            messages = messages.filter(id__gt=int(after))
        rows = [serialize_message(m, request.user) for m in messages]
        if rows:
            _mark_read(thread, request.user)
        return Response(rows)

    def post(self, request, thread_id):
        lang = get_language(request)
        thread = _thread_for(request.user, thread_id)
        body, err = validate_message_body(request.data, lang)
        if err:
            return Response(err, status=400)
        message = _append_message(thread, request.user, body)
        return Response(serialize_message(message, request.user), status=201)
