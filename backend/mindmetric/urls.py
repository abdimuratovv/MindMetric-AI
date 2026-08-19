"""
Root URL conf. Each app owns its own `/api/<app>/...` namespace so the
mapping in ARCHITECTURE.md §2 stays traceable straight from this file.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/public/', include('apps.analytics.public_urls')),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/accounts/', include('apps.accounts.urls_profile')),
    path('api/assessments/', include('apps.assessments.urls')),
    path('api/results/', include('apps.scoring.urls')),
    path('api/achievements/', include('apps.scoring.urls_achievements')),
    path('api/teacher/', include('apps.reviews.urls')),
    path('api/admin/', include('apps.analytics.urls')),
    path('api/videocalls/', include('apps.videocalls.urls')),
]
