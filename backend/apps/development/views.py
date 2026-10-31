from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from apps.accounts.permissions import HasCompletedProfile, IsStudent
from apps.i18n import get_language
from .models import DevelopmentEnrollment, DevelopmentModule, DevelopmentSession
from .permissions import STUDENT_PERMISSIONS
from . import progress
from .recommendations import build_plan, visible_catalogue
from .translations import ContentLocale
from .curriculum import cluster_cards
from .serializers import (
    AnswerSerializer, HintSerializer, StartSessionSerializer, enrollment_state, feedback, module_card, session_state,
)


class DevelopmentView(APIView):
    permission_classes = STUDENT_PERMISSIONS
    throttle_classes = [ScopedRateThrottle]

    def handle_exception(self, exc):
        if isinstance(exc, progress.FlowError):
            return Response({'detail': progress.ERRORS[get_language(self.request)][exc.flow_code],
                             'code': exc.flow_code}, status=exc.status_code)
        return super().handle_exception(exc)

    def enrollment(self, pk):
        obj = get_object_or_404(DevelopmentEnrollment.objects.select_related('module'), pk=pk, student=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def session(self, pk):
        obj = get_object_or_404(DevelopmentSession.objects.select_related('enrollment__module'),
                                pk=pk, enrollment__student=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class CapabilitiesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent, HasCompletedProfile]

    def get(self, request):
        enabled = settings.DEVELOPMENT_CLUSTER1_ENABLED
        return Response({'enabled': enabled, 'available': enabled and DevelopmentModule.objects.filter(status='published').exists()})


class ModuleListView(DevelopmentView):
    def get(self, request):
        modules, enrolled = visible_catalogue(request.user)
        return Response({'modules': [module_card(module, enrolled.get(module.key),get_language(request)) for module in modules],
                         'clusters': cluster_cards(modules, get_language(request))})


class PlanView(DevelopmentView):
    def get(self, request):
        plan = build_plan(request.user, get_language(request))

        def card(entry):
            return {**module_card(entry['module'], entry['enrollment'],get_language(request)),
                    'recommendation': entry['recommendation'], 'skills': ContentLocale(entry['module'],get_language(request)).progress(entry['skills'])}

        return Response({
            'recommended': [card(row) for row in plan['recommended']],
            'modules': [card(row) for row in plan['entries']],
            'check_active': plan['check_active'], 'active_enrollment_id': plan['active_enrollment_id'],
            'minimum_diagnostic_responses': plan['minimum_diagnostic_responses'],
            'clusters': cluster_cards([row['module'] for row in plan['entries']], get_language(request)),
        })


class EnrollView(DevelopmentView):
    throttle_scope = 'development-session'

    def post(self, request, key):
        row = progress.enroll(request.user, key)
        self.check_object_permissions(request, row)
        return Response(enrollment_state(row,get_language(request)))


class EnrollmentView(DevelopmentView):
    def get(self, request, pk):
        return Response(enrollment_state(self.enrollment(pk),get_language(request)))


class LessonCompleteView(DevelopmentView):
    throttle_scope = 'development-answer'

    def post(self, request, pk, key):
        self.enrollment(pk)
        return Response(enrollment_state(progress.complete_lesson(request.user, pk, key),get_language(request)))


class SessionStartView(DevelopmentView):
    throttle_scope = 'development-session'

    def post(self, request, pk):
        self.enrollment(pk)
        serializer = StartSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(session_state(progress.start_session(request.user, pk, serializer.validated_data['purpose']),get_language(request)))


class SessionNextView(DevelopmentView):
    def get(self, request, pk):
        return Response(session_state(self.session(pk),get_language(request)))


class AnswerView(DevelopmentView):
    throttle_scope = 'development-answer'

    def post(self, request, pk):
        self.session(pk)
        serializer = AnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session, answer = progress.submit_answer(request.user, pk, language=get_language(request), **serializer.validated_data)
        result = {'accepted': True, 'session': session_state(session,get_language(request))}
        if session.purpose == 'practice' and not progress.live_check(session.enrollment):
            result['feedback'] = feedback(session, answer,get_language(request))
        return Response(result)


class HintView(DevelopmentView):
    throttle_scope = 'development-answer'

    def post(self, request, pk):
        self.session(pk)
        serializer = HintSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        key=serializer.validated_data['exercise_key']
        original=progress.request_hint(request.user, pk, key)
        locale=ContentLocale(self.session(pk).enrollment.module,get_language(request))
        translated=locale.exercise(key)
        return Response({'hint':translated['hint'] if translated else original,'content_language':locale.language})


class FinishView(DevelopmentView):
    throttle_scope = 'development-session'

    def post(self, request, pk):
        self.session(pk)
        session = progress.finish_session(request.user, pk)
        return Response({'session': session_state(session,get_language(request)), 'enrollment': enrollment_state(session.enrollment,get_language(request))})


class ProgressView(DevelopmentView):
    def get(self, request):
        return Response({'enrollments': [enrollment_state(row,get_language(request)) for row in
                         DevelopmentEnrollment.objects.filter(student=request.user).select_related('module').order_by('-started_at')]})
