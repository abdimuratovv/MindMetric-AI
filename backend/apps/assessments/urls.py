from django.urls import path

from . import views

urlpatterns = [
    path('status/', views.AssessmentStatusView.as_view(), name='assessment-status'),

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

    # Likert pattern: teamwork, patience, learning_speed
    path('likert/<str:kind>/start/', views.StartLikertAttemptView.as_view(), name='likert-start'),
    path('likert/<str:kind>/items/', views.LikertItemsView.as_view(), name='likert-items'),
    path('likert/<str:kind>/answer/', views.AnswerLikertView.as_view(), name='likert-answer'),
    path('likert/<str:kind>/submit/', views.SubmitLikertView.as_view(), name='likert-submit'),

    path('<str:assessment_type>/pause/', views.PauseAttemptView.as_view(), name='attempt-pause'),
]
