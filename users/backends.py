import datetime

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import F

from .models import PhoneToken

User = get_user_model()


class EmailPhoneBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            phone = kwargs.get('phone')
            if phone is None:
                return None
            else:
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    return None
        else:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


class Phone2FABackend(ModelBackend):
    def authenticate(self, request, pk=None, otp=None, **kwargs):
        if pk is None:
            return None

        timestamp_difference = datetime.datetime.now() - datetime.timedelta(
            minutes=getattr(settings, 'PHONE_LOGIN_MINUTES', 10))

        try:
            phone_token = PhoneToken.objects.get(
                pk=pk,
                otp=otp,
                used=False,
                timestamp__gte=timestamp_difference)

        except PhoneToken.DoesNotExist:
            phone_token = PhoneToken.objects.get(pk=pk)
            phone_token.attempts = F('attempts') + 1
            phone_token.save()
            raise PhoneToken.DoesNotExist

        try:
            user = User.objects.get(phone=phone_token.phone)
        except User.DoesNotExist:
            return None

        phone_token.used = True
        phone_token.attempts = F('attempts') + 1
        phone_token.save()

        return user