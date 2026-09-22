import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

# Hard caps enforced in serializers.py and mirrored by the composer's
# maxLength in the frontend — a support thread is a short bug report or an
# idea, not an essay, and the body is rendered as plain text either way.
SUBJECT_MAX_LENGTH = 140
BODY_MAX_LENGTH = 2000

# Screenshot limits. The frontend already downscales to 1600px and re-encodes
# as WebP (components/ScreenshotDropzone.jsx), which puts a typical screenshot
# around 150-250KB — this cap is the server-side backstop, not the target.
MAX_ATTACHMENTS_PER_MESSAGE = 3
MAX_ATTACHMENT_BYTES = 1_500_000

# Only these three are stored, and the type is decided by sniffing the bytes
# (see serializers.sniff_image_type) rather than trusting the upload's declared
# Content-Type — the value below is what we later serve the file back as.
ALLOWED_IMAGE_TYPES = ('image/webp', 'image/png', 'image/jpeg')


class SupportThread(models.Model):
    """
    One student↔admin conversation about the platform itself (a bug, an idea,
    a question) — the written counterpart to apps.videocalls, opened from the
    student's "Yordam" screen and worked through the admin's support inbox.

    Threaded rather than a flat message feed because the admin side is managed
    by "which report is still unanswered", not by "who wrote last" — the same
    queue shape as apps.reviews.TeacherReview.
    """

    class Category(models.TextChoices):
        BUG = 'bug', 'Bug report'
        IDEA = 'idea', 'Improvement idea'
        FEEDBACK = 'feedback', 'General feedback'
        QUESTION = 'question', 'Question'

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'            # waiting on an admin
        ANSWERED = 'answered', 'Answered'  # admin replied, waiting on the student
        RESOLVED = 'resolved', 'Resolved'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='support_threads', on_delete=models.CASCADE,
    )
    # The admin the student picked, or null for "any admin" — the shared queue.
    # Null is the deliberate default: a thread addressed to one absent admin
    # would otherwise sit unanswered with nobody else treating it as theirs.
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='support_assigned', on_delete=models.SET_NULL,
        null=True, blank=True,
    )

    category = models.CharField(max_length=10, choices=Category.choices, default=Category.BUG)
    subject = models.CharField(max_length=SUBJECT_MAX_LENGTH)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    created_at = models.DateTimeField(auto_now_add=True)
    # Denormalized from the last SupportMessage so the inbox can sort without
    # a join, and so the unread dot doesn't cost a COUNT(*) per row on every
    # poll — the list is the most frequently hit endpoint of this app.
    last_message_at = models.DateTimeField(default=timezone.now, db_index=True)
    student_unread = models.PositiveSmallIntegerField(default=0)
    admin_unread = models.PositiveSmallIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['assignee', 'status', '-last_message_at']),
            models.Index(fields=['student', '-last_message_at']),
        ]

    def __str__(self):
        return f'#{self.pk} {self.subject}'

    def unread_for(self, user) -> int:
        from apps.accounts.models import User
        return self.admin_unread if user.role == User.Role.ADMIN else self.student_unread


class SupportMessage(models.Model):
    """One entry in a SupportThread, from either side. `author` is nullable so
    deleting a staff account keeps the conversation history readable."""

    thread = models.ForeignKey(SupportThread, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='support_messages', on_delete=models.SET_NULL, null=True,
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        indexes = [
            models.Index(fields=['thread', 'id']),
        ]

    def __str__(self):
        return f'{self.thread_id}:{self.pk}'


class SupportAttachment(models.Model):
    """
    A screenshot attached to a SupportMessage, stored as bytea in Postgres.

    Deliberately not a FileField: Render's filesystem is ephemeral (an uploaded
    file would vanish on the next deploy) and the project has no S3/Cloudinary
    credentials — see render.yaml. The bytes are small and strictly capped, and
    moving to object storage later is a STORAGES swap plus a data migration.

    Served only through apps.support.views.AttachmentView, which re-checks the
    thread's permissions — there is no public URL. The primary key is a UUID so
    an id can't be walked to probe for other students' screenshots.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(SupportMessage, related_name='attachments', on_delete=models.CASCADE)
    data = models.BinaryField()
    content_type = models.CharField(max_length=40)
    byte_size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.id} ({self.byte_size} B)'
