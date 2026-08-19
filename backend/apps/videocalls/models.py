import uuid

from django.conf import settings
from django.db import models


def _generate_room_name():
    return uuid.uuid4().hex


class VideoCall(models.Model):
    """
    One teacher↔student LiveKit room, started from the admin's Review Queue
    (apps.reviews) and joined by the student via short polling on the
    frontend (no WebSockets in this stack — see apps.videocalls.views).
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACTIVE = 'active', 'Active'
        ENDED = 'ended', 'Ended'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='video_calls_as_student', on_delete=models.CASCADE,
    )
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='video_calls_started', on_delete=models.SET_NULL, null=True,
    )

    room_name = models.CharField(max_length=64, unique=True, default=_generate_room_name, editable=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.room_name} ({self.status})'
