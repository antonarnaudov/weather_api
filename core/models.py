import re

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


def validate_phone(phone):
    regex = r"(\+\d{1,3}\s?)?((\(\d{3}\)\s?)|(\d{3})(\s|-?))(\d{3}(\s|-?))(\d{4})(\s?(([E|e]xt[:|.|]?)|x|X)(\s?\d+))?"
    if not re.fullmatch(regex, phone):
        raise ValidationError(f'This is not a valid phone number: {phone}')


class Extended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField("Phone Number", max_length=50, null=True, blank=True)

    def clean(self):
        if self.phone:
            validate_phone(self.phone)

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
