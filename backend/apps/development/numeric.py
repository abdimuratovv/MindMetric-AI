"""Bounded exact numeric input, shared by content validation and future grading."""

import re
from fractions import Fraction


def parse_numeric(value):
    if not isinstance(value, str) or len(value) > 80:
        raise ValueError('Enter a number or fraction of at most 80 characters.')
    value = value.strip().replace(',', '.')
    if sum(character.isdigit() for character in value) > 40:
        raise ValueError('Too many digits.')
    if '/' in value:
        parts = value.split('/')
        if len(parts) != 2 or not all(re.fullmatch(r'[+-]?[0-9]+', part.strip()) for part in parts):
            raise ValueError('Enter one fraction, without expressions.')
        numerator, denominator = (int(part.strip()) for part in parts)
        if denominator == 0:
            raise ValueError('Denominator must not be zero.')
        return Fraction(numerator, denominator)
    if not re.fullmatch(r'[+-]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)', value):
        raise ValueError('Enter an integer, decimal or fraction, without expressions.')
    return Fraction(value)
