from django.urls import path

from . import views

urlpatterns = [
    path('status/', views.AssessmentStatusView.as_view(), name='assessment-status'),
    path('config/', views.AssessmentConfigView.as_view(), name='assessment-config'),

    # MCQ pattern: math, logic, creative, problem_solving, attention, iq
    path('mcq/<str:kind>/start/', views.StartMcqAttemptView.as_view(), name='mcq-start'),
    path('mcq/<str:kind>/next-question/', views.NextMcqQuestionView.as_view(), name='mcq-next-question'),
    path('mcq/<str:kind>/answer/', views.AnswerMcqView.as_view(), name='mcq-answer'),
    path('mcq/<str:kind>/submit/', views.SubmitMcqView.as_view(), name='mcq-submit'),

    # Coding pattern: algorithmic (the only member)
    path('coding/problem/', views.CodingProblemView.as_view(), name='coding-problem'),
    path('coding/start/', views.StartCodingView.as_view(), name='coding-start'),
    path('coding/run/', views.RunCodingView.as_view(), name='coding-run'),
    path('coding/submit/', views.SubmitCodingView.as_view(), name='coding-submit'),

    # Learning pattern: learning_speed
    path('learning/start/', views.StartLearningView.as_view(), name='learning-start'),
    path('learning/state/', views.LearningStateView.as_view(), name='learning-state'),
    path('learning/answer/', views.AnswerLearningView.as_view(), name='learning-answer'),
    path('learning/submit/', views.SubmitLearningView.as_view(), name='learning-submit'),

    # SJT pattern: teamwork
    path('sjt/start/', views.StartSjtView.as_view(), name='sjt-start'),
    path('sjt/next/', views.NextSjtView.as_view(), name='sjt-next'),
    path('sjt/answer/', views.AnswerSjtView.as_view(), name='sjt-answer'),
    path('sjt/submit/', views.SubmitSjtView.as_view(), name='sjt-submit'),

    # Anagram pattern: patience
    path('anagram/start/', views.StartAnagramView.as_view(), name='anagram-start'),
    path('anagram/current/', views.CurrentAnagramView.as_view(), name='anagram-current'),
    path('anagram/guess/', views.GuessAnagramView.as_view(), name='anagram-guess'),
    path('anagram/skip/', views.SkipAnagramView.as_view(), name='anagram-skip'),
    path('anagram/submit/', views.SubmitAnagramView.as_view(), name='anagram-submit'),

    path('<str:assessment_type>/pause/', views.PauseAttemptView.as_view(), name='attempt-pause'),
]
