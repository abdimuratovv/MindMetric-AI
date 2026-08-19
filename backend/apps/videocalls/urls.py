from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.StartCallView.as_view(), name='videocall-start'),
    path('active/', views.ActiveCallView.as_view(), name='videocall-active'),
    path('<int:call_id>/join/', views.JoinCallView.as_view(), name='videocall-join'),
    path('<int:call_id>/end/', views.EndCallView.as_view(), name='videocall-end'),
]
