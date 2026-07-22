from django.urls import path

from . import views

urlpatterns = [
    path('stats/', views.PublicStatsView.as_view(), name='public-stats'),
]
