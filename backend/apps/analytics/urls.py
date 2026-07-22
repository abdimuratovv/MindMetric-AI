from django.urls import path

from . import views

urlpatterns = [
    path('kpis/', views.AdminKpiView.as_view(), name='admin-kpis'),
    path('distribution/', views.CohortDistributionView.as_view(), name='admin-distribution'),
    path('field-distribution/', views.FieldDistributionView.as_view(), name='admin-field-distribution'),
    path('faculty-activity/', views.FacultyActivityView.as_view(), name='admin-faculty-activity'),
    path('students/', views.AdminStudentListView.as_view(), name='admin-students'),
    path('question-bank/', views.QuestionBankView.as_view(), name='admin-question-bank'),
    path('question-bank/mcq/', views.QuestionBankMcqListView.as_view(), name='admin-question-bank-mcq-list'),
    path('question-bank/mcq/<int:pk>/', views.QuestionBankMcqDetailView.as_view(), name='admin-question-bank-mcq-detail'),
    path('question-bank/likert/', views.QuestionBankLikertListView.as_view(), name='admin-question-bank-likert-list'),
    path('question-bank/likert/<int:pk>/', views.QuestionBankLikertDetailView.as_view(), name='admin-question-bank-likert-detail'),
]
