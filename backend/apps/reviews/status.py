"""Ported from the mockup's `statusStyle()` (line 957), translated ru/uz —
shared by the teacher queue and the admin student table, both of which render
the same {{ s.statusBg }}/{{ s.statusColor }}/{{ s.statusLabel }} badge."""

_LABELS = {
    'reviewed': {'ru': 'Проверено', 'uz': 'Koʼrib chiqilgan'},
    'flagged': {'ru': 'Отмечено', 'uz': 'Belgilangan'},
    'pending': {'ru': 'Ожидает', 'uz': 'Kutilmoqda'},
}


def status_style(status: str, lang: str) -> dict:
    if status == 'reviewed':
        return {'bg': '#DCEFE2', 'color': '#1F4B39', 'label': _LABELS['reviewed'][lang]}
    if status == 'flagged':
        return {'bg': '#F6E0DC', 'color': '#BD5B4C', 'label': _LABELS['flagged'][lang]}
    return {'bg': '#F5E9D3', 'color': '#B8862F', 'label': _LABELS['pending'][lang]}
