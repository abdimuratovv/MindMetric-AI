from django.urls import path

from . import views

urlpatterns = [
    path('summary/', views.ResultsSummaryView.as_view(), name='results-summary'),
    path('analytics/', views.AnalyticsDetailView.as_view(), name='results-analytics'),
    path('mistakes/', views.ResultsMistakesView.as_view(), name='results-mistakes'),
]
