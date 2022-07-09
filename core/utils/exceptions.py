from django.core.exceptions import ObjectDoesNotExist
from django.db import ProgrammingError, IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError as EmailValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Custom Error Exception Handler"""
    response = exception_handler(exc, context)

    error_400_list = [ValidationError, ValueError, IntegrityError, ObjectDoesNotExist, KeyError, AttributeError,
                      EmailValidationError]
    error_404_list = [ProgrammingError, Http404]

    if response is None:
        if any([isinstance(exc, error) for error in error_404_list]):
            response = Response(str(exc), status=status.HTTP_404_NOT_FOUND)

        if any([isinstance(exc, error) for error in error_400_list]):
            response = Response(str(exc), status=status.HTTP_400_BAD_REQUEST)
    return response
