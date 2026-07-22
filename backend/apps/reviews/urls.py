from django.urls import path

from . import views

urlpatterns = [
    path('students/', views.TeacherStudentListView.as_view(), name='teacher-students'),
    path('students/<int:student_id>/', views.TeacherStudentDetailView.as_view(), name='teacher-student-detail'),
    path('students/<int:student_id>/review/', views.SubmitReviewView.as_view(), name='teacher-submit-review'),
]
