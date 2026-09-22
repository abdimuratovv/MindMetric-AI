from django.urls import path

from . import views

urlpatterns = [
    path('options/', views.SupportOptionsView.as_view(), name='support-options'),
    path('threads/', views.ThreadListCreateView.as_view(), name='support-threads'),
    path('threads/<int:thread_id>/', views.ThreadDetailView.as_view(), name='support-thread-detail'),
    path('threads/<int:thread_id>/messages/', views.ThreadMessagesView.as_view(), name='support-thread-messages'),
]
