"""
Input validation and response shaping for apps.support.

Validation errors come back as {'detail': '<translated>'} — the shape
frontend/src/api/client.js surfaces verbatim — rather than DRF's field-keyed
error dict, matching apps.assessments.views' ANSWER_REQUIRED handling.
"""

from apps.accounts.models import User

from .labels import attachment_preview, category_label, status_style
from .models import (
    BODY_MAX_LENGTH,
    MAX_ATTACHMENT_BYTES,
    MAX_ATTACHMENTS_PER_MESSAGE,
    SUBJECT_MAX_LENGTH,
    SupportThread,
)

ERRORS = {
    'subject_required': {
        'ru': 'Укажите тему обращения.',
        'uz': 'Murojaat mavzusini kiriting.',
    },
    'body_required': {
        'ru': 'Опишите обращение.',
        'uz': 'Murojaatingizni yozing.',
    },
    'body_too_long': {
        'ru': f'Сообщение не может быть длиннее {BODY_MAX_LENGTH} символов.',
        'uz': f"Xabar {BODY_MAX_LENGTH} belgidan uzun bo'lishi mumkin emas.",
    },
    'invalid_category': {
        'ru': 'Выберите категорию обращения.',
        'uz': 'Murojaat turini tanlang.',
    },
    'invalid_assignee': {
        'ru': 'Выбранный администратор недоступен.',
        'uz': 'Tanlangan administrator mavjud emas.',
    },
    'invalid_status': {
        'ru': 'Недопустимый статус.',
        'uz': 'Yaroqsiz holat.',
    },
    # Surfaced instead of DRF's English "Request was throttled" default —
    # the product ships ru/uz only (see apps.i18n).
    'too_many_threads': {
        'ru': 'Вы создали слишком много обращений за сегодня. Продолжите в уже открытом обращении.',
        'uz': "Bugun juda ko'p murojaat yaratdingiz. Ochiq murojaatingizda davom eting.",
    },
    'too_many_messages': {
        'ru': 'Слишком много сообщений подряд. Попробуйте чуть позже.',
        'uz': "Ketma-ket juda ko'p xabar yuborildi. Birozdan so'ng urinib ko'ring.",
    },
    'too_many_files': {
        'ru': f'Можно приложить не больше {MAX_ATTACHMENTS_PER_MESSAGE} изображений к одному сообщению.',
        'uz': f"Bitta xabarga ko'pi bilan {MAX_ATTACHMENTS_PER_MESSAGE} ta rasm biriktirish mumkin.",
    },
    'file_too_large': {
        'ru': 'Изображение слишком большое — до 1,5 МБ.',
        'uz': "Rasm hajmi juda katta — 1,5 MB gacha.",
    },
    'file_not_image': {
        'ru': 'Поддерживаются только изображения PNG, JPEG и WebP.',
        'uz': 'Faqat PNG, JPEG va WebP rasmlari qabul qilinadi.',
    },
}


def error(key: str, lang: str) -> dict:
    return {'detail': ERRORS[key][lang]}


def _resolve_assignee(raw):
    """`assignee_id` is optional — an absent/empty value means the shared
    "any admin" queue. Returns (admin_or_None, ok)."""
    if raw in (None, '', 0, '0'):
        return None, True
    admin = User.objects.filter(id=raw, role=User.Role.ADMIN).first()
    return admin, admin is not None


def validate_thread_payload(data, lang: str, *, allow_empty_body=False):
    """Returns (cleaned_dict, error_response_or_None) for POST /threads/."""
    category = data.get('category')
    if category not in SupportThread.Category.values:
        return None, error('invalid_category', lang)

    subject = (data.get('subject') or '').strip()
    if not subject:
        return None, error('subject_required', lang)

    # A new thread always carries a subject, so its first message may be a bare
    # screenshot — the subject already says what it's about.
    body, body_error = validate_message_body(data, lang, allow_empty=allow_empty_body)
    if body_error:
        return None, body_error

    assignee, ok = _resolve_assignee(data.get('assignee_id'))
    if not ok:
        return None, error('invalid_assignee', lang)

    return {
        'category': category,
        'subject': subject[:SUBJECT_MAX_LENGTH],
        'body': body,
        'assignee': assignee,
    }, None


def validate_message_body(data, lang: str, *, allow_empty=False):
    """Returns (body, error_response_or_None) — shared by thread creation and
    replies. `allow_empty` is passed when the message carries a screenshot: a
    pasted screenshot with no words is a legitimate bug report."""
    body = (data.get('body') or '').strip()
    if not body and not allow_empty:
        return None, error('body_required', lang)
    if len(body) > BODY_MAX_LENGTH:
        return None, error('body_too_long', lang)
    return body, None


# Magic numbers for the three accepted formats. Sniffing the bytes rather than
# adding Pillow keeps the Render build lean, and it's the stricter check anyway:
# a request can claim any Content-Type, but it can't fake the file header of a
# format we then serve back under exactly that type (with nosniff, see
# views.AttachmentView).
_PNG = b'\x89PNG\r\n\x1a\n'
_JPEG = b'\xff\xd8\xff'


def sniff_image_type(data: bytes):
    """The image's real media type, or None if these bytes aren't one we accept."""
    if data.startswith(_PNG):
        return 'image/png'
    if data.startswith(_JPEG):
        return 'image/jpeg'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'image/webp'
    return None


def validate_attachments(files, lang: str):
    """
    Turns the uploaded files into [(bytes, content_type)], or returns an error.

    `files` is request.FILES.getlist('attachments') — an empty list is valid
    (most messages are plain text).
    """
    if len(files) > MAX_ATTACHMENTS_PER_MESSAGE:
        return None, error('too_many_files', lang)

    cleaned = []
    for upload in files:
        if upload.size > MAX_ATTACHMENT_BYTES:
            return None, error('file_too_large', lang)
        data = upload.read()
        content_type = sniff_image_type(data)
        if content_type is None:
            return None, error('file_not_image', lang)
        cleaned.append((data, content_type))
    return cleaned, None


def _person(user) -> dict:
    if user is None:
        return None
    return {
        'id': user.id,
        'name': user.get_full_name() or user.email,
        'initials': user.initials,
    }


def serialize_message(message, viewer) -> dict:
    author = message.author
    return {
        'id': message.id,
        'body': message.body,
        'createdAt': message.created_at.isoformat(),
        'authorName': (author.get_full_name() or author.email) if author else '',
        'authorInitials': author.initials if author else '',
        'authorRole': author.role if author else '',
        # Drives which side of the conversation the bubble sits on, so the
        # shared SupportThreadView doesn't need to know the viewer's role.
        'mine': bool(author and author.id == viewer.id),
        # `url` is an API path, not a public link — the frontend fetches it with
        # the JWT attached and renders the blob (see api/client.js fetchBlobUrl).
        'attachments': [
            {'id': str(a.id), 'url': f'/support/attachments/{a.id}/', 'byteSize': a.byte_size}
            for a in message.attachments.all()
        ],
    }


def _preview(last_message, lang: str) -> str:
    """The list row's one-line summary. A screenshot-only message has no text to
    show, so it falls back to a translated "image" marker."""
    if last_message is None:
        return ''
    if last_message.body:
        return last_message.body[:120]
    return attachment_preview(lang)


def serialize_thread_row(thread, lang: str, viewer, last_message=None) -> dict:
    style = status_style(thread.status, lang)
    student = thread.student
    return {
        'id': thread.id,
        'subject': thread.subject,
        'category': thread.category,
        'categoryLabel': category_label(thread.category, lang),
        'status': thread.status,
        'statusLabel': style['label'], 'statusBg': style['bg'], 'statusColor': style['color'],
        'createdAt': thread.created_at.isoformat(),
        'lastMessageAt': thread.last_message_at.isoformat(),
        'preview': _preview(last_message, lang),
        'unread': thread.unread_for(viewer),
        'student': {**_person(student), 'program': student.program},
        'assignee': _person(thread.assignee),
    }


def serialize_thread_detail(thread, lang: str, viewer, messages) -> dict:
    return {
        **serialize_thread_row(thread, lang, viewer, last_message=messages[-1] if messages else None),
        'messages': [serialize_message(m, viewer) for m in messages],
    }
