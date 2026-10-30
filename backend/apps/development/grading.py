from rest_framework.exceptions import ValidationError

from .numeric import parse_numeric


def grade(question, response, language='uz'):
    def invalid(uz, ru):
        return ValidationError({'detail': ru if language == 'ru' else uz})

    if not isinstance(response, dict):
        raise invalid('Javob obyekt ko‘rinishida bo‘lishi kerak.', 'Ответ должен быть объектом.')
    if question['format'] == 'numeric':
        if set(response) != {'value'}:
            raise invalid('Son yoki kasr kiriting.', 'Введите число или дробь.')
        try:
            return float(parse_numeric(response['value']) == parse_numeric(question['answer_key']['value']))
        except ValueError as exc:
            raise invalid('Butun son, o‘nli son yoki bitta kasr kiriting; maxraj nol bo‘lmasin.',
                          'Введите целое число, десятичную дробь или одну обыкновенную дробь; знаменатель не должен быть нулём.') from exc
    if question['format'] == 'single':
        if set(response) != {'option_id'} or not isinstance(response['option_id'], str) or response['option_id'] not in {o['id'] for o in question['options']}:
            raise invalid('Mavjud variantlardan birini tanlang.', 'Выберите один из предложенных вариантов.')
        return float(response['option_id'] == question['answer_key']['option_id'])
    raise invalid('Ushbu savol formati hali qo‘llanmaydi.', 'Этот формат задания пока не поддерживается.')
