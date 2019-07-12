from django.contrib.auth import get_user_model
from django.core import validators
from django.core.cache import cache
from django.utils.deconstruct import deconstructible

from rest_framework.exceptions import AuthenticationFailed, ValidationError


@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r'^\d+$'
    message = 'Incorrect phone format. Should contain numbers only.'
    flags = 0


class PhoneUniqueValidator(PhoneValidator):

    def __call__(self, value):
        super().__call__(value)
        if get_user_model().objects.filter(phone=value).exists():
            raise ValidationError('User with this phone already exists')


def validate_code(code, phone):
    if code != cache.get(phone):
        raise AuthenticationFailed('Invalid or expired code')
    cache.delete(phone)
