from django.core.exceptions import ValidationError


def always_zero(value):
    if value not in ["0", 0]:
        raise ValidationError("Warning: Here should be always a zero")


def always_star(value):
    if value != "*":
        raise ValidationError('Warning: Here should be always a "*"')
