from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class SendEmailError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Send Email Error')
    default_code = 'send_email_error'
