"""
Server-side ru/uz copy for everything the support screens render as a badge
or a dropdown option. Same convention as apps.reviews.status: the stable
key is what's stored, the label is resolved per request from the X-Language
header (apps.i18n.get_language), so the frontend never duplicates it.

Colours are reused from the existing status badges (apps.reviews.status) so
the support inbox reads as part of the same admin surface.
"""

from .models import SupportThread

_STATUS = {
    SupportThread.Status.OPEN: {
        'bg': '#F5E9D3', 'color': '#B8862F',
        'ru': 'Ожидает ответа', 'uz': 'Javob kutilmoqda',
    },
    SupportThread.Status.ANSWERED: {
        'bg': '#DCECEF', 'color': '#1F374B',
        'ru': 'Есть ответ', 'uz': 'Javob berilgan',
    },
    SupportThread.Status.RESOLVED: {
        'bg': '#DCEFE2', 'color': '#1F4B39',
        'ru': 'Решено', 'uz': 'Hal qilingan',
    },
}

_CATEGORY = {
    SupportThread.Category.BUG: {'ru': 'Ошибка', 'uz': 'Xatolik'},
    SupportThread.Category.IDEA: {'ru': 'Идея по улучшению', 'uz': 'Yaxshilash gʼoyasi'},
    SupportThread.Category.FEEDBACK: {'ru': 'Отзыв о платформе', 'uz': 'Platforma haqida fikr'},
    SupportThread.Category.QUESTION: {'ru': 'Вопрос', 'uz': 'Savol'},
}


_ATTACHMENT_PREVIEW = {'ru': '📎 Изображение', 'uz': '📎 Rasm'}


def attachment_preview(lang: str) -> str:
    """Stands in for the list-row preview of a message that is only a screenshot."""
    return _ATTACHMENT_PREVIEW[lang]


def status_style(status: str, lang: str) -> dict:
    entry = _STATUS.get(status, _STATUS[SupportThread.Status.OPEN])
    return {'bg': entry['bg'], 'color': entry['color'], 'label': entry[lang]}


def category_label(category: str, lang: str) -> str:
    entry = _CATEGORY.get(category, _CATEGORY[SupportThread.Category.BUG])
    return entry[lang]


def category_options(lang: str) -> list:
    """Feeds the student composer's category chips — ordered as declared on the model."""
    return [
        {'key': key, 'label': _CATEGORY[key][lang]}
        for key, _ in SupportThread.Category.choices
    ]


def status_options(lang: str) -> list:
    """Feeds the admin inbox's status filter and the resolve/reopen control."""
    return [
        {'key': key, 'label': _STATUS[key][lang], 'bg': _STATUS[key]['bg'], 'color': _STATUS[key]['color']}
        for key, _ in SupportThread.Status.choices
    ]
