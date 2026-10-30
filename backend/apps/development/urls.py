from django.urls import path

from . import views

urlpatterns = [
    path('capabilities/', views.CapabilitiesView.as_view()),
    path('modules/', views.ModuleListView.as_view()),
    path('plan/', views.PlanView.as_view()),
    path('modules/<slug:key>/enroll/', views.EnrollView.as_view()),
    path('enrollments/<int:pk>/', views.EnrollmentView.as_view()),
    path('enrollments/<int:pk>/lessons/<slug:key>/complete/', views.LessonCompleteView.as_view()),
    path('enrollments/<int:pk>/sessions/', views.SessionStartView.as_view()),
    path('sessions/<int:pk>/next/', views.SessionNextView.as_view()),
    path('sessions/<int:pk>/answers/', views.AnswerView.as_view()),
    path('sessions/<int:pk>/hints/', views.HintView.as_view()),
    path('sessions/<int:pk>/finish/', views.FinishView.as_view()),
    path('progress/', views.ProgressView.as_view()),
]
