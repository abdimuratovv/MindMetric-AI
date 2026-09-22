"""
Input validation and response shaping for apps.support.

Validation errors come back as {'detail': '<translated>'} — the shape
frontend/src/api/client.js surfaces verbatim — rather than DRF's field-keyed
error dict, matching apps.assessments.views' ANSWER_REQUIRED handling.
"""

from apps.accounts.models import User

from .labels import category_label, status_style
from .models import BODY_MAX_LENGTH, SUBJECT_MAX_LENGTH, SupportThread

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


def validate_thread_payload(data, lang: str):
    """Returns (cleaned_dict, error_response_or_None) for POST /threads/."""
    category = data.get('category')
    if category not in SupportThread.Category.values:
        return None, error('invalid_category', lang)

    subject = (data.get('subject') or '').strip()
    if not subject:
        return None, error('subject_required', lang)

    body, body_error = validate_message_body(data, lang)
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


def validate_message_body(data, lang: str):
    """Returns (body, error_response_or_None) — shared by thread creation and replies."""
    body = (data.get('body') or '').strip()
    if not body:
        return None, error('body_required', lang)
    if len(body) > BODY_MAX_LENGTH:
        return None, error('body_too_long', lang)
    return body, None


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
    }


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
        'preview': (last_message.body[:120] if last_message else ''),
        'unread': thread.unread_for(viewer),
        'student': {**_person(student), 'program': student.program},
        'assignee': _person(thread.assignee),
    }


def serialize_thread_detail(thread, lang: str, viewer, messages) -> dict:
    return {
        **serialize_thread_row(thread, lang, viewer, last_message=messages[-1] if messages else None),
        'messages': [serialize_message(m, viewer) for m in messages],
    }
