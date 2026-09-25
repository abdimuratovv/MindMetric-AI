from django.urls import path

from . import views

urlpatterns = [
    path('me/', views.MeView.as_view(), name='me'),
    path('complete-profile/', views.CompleteProfileView.as_view(), name='complete-profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('sign-out-everywhere/', views.SignOutEverywhereView.as_view(), name='sign-out-everywhere'),
]
