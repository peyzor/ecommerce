import datetime
import hashlib
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field.modelfields import PhoneNumberField
from kavenegar import KavenegarAPI, APIException, HTTPException


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError(_('Users should have a username'))

        if email is None:
            raise TypeError(_('Users should have an Email'))

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError(_('Password should not be None'))

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'),
                                max_length=255,
                                unique=True,
                                db_index=True)
    email = models.EmailField(_('email'),
                              max_length=255,
                              unique=True,
                              db_index=True)
    phone = PhoneNumberField(_('phone'), blank=True, null=True, unique=True)
    is_verified = models.BooleanField(_('is verified'), default=False)
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        tokens_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return tokens_data

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')


class PhoneToken(models.Model):
    phone = PhoneNumberField(_('phone'), editable=False)
    otp = models.CharField(_('otp'), max_length=40, editable=False)
    timestamp = models.DateTimeField(_('timestamp'),
                                     auto_now_add=True,
                                     editable=False)
    attempts = models.IntegerField(_('attempts'), default=0)
    used = models.BooleanField(_('used'), default=False)

    class Meta:
        db_table = 'phone_token'
        verbose_name = _("otp token")
        verbose_name_plural = _("otp tokens")

    def __str__(self):
        return f'{self.phone}, {self.otp}'

    @classmethod
    def create_otp_for_number(cls, number):
        # The max otps generated for a number in a day are only 10.
        # Any more than 10 attempts returns False for the day.
        today_min = datetime.datetime.combine(datetime.date.today(),
                                              datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(),
                                              datetime.time.max)

        otps = cls.objects.filter(phone=number,
                                  timestamp__range=(today_min, today_max))

        if otps.count() <= getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 30):
            otp = cls.generate_otp(
                length=getattr(settings, 'PHONE_LOGIN_OTP_LENGTH', 6))

            phone_token = PhoneToken(phone=number, otp=otp)
            phone_token.save()

            api_key = settings.API_KEY
            try:
                api = KavenegarAPI(api_key)
                params = {
                    'sender': '10004346',
                    'receptor': number,
                    'message': f'Your code: {otp}'
                }
                api.sms_send(params)
                return phone_token

            except APIException:
                return None

            except HTTPException:
                return None

        return None

    @classmethod
    def generate_otp(cls, length=6):
        hash_algorithm = getattr(settings, 'PHONE_LOGIN_OTP_HASH_ALGORITHM',
                                 'sha256')
        m = getattr(hashlib, hash_algorithm)()
        m.update(getattr(settings, 'SECRET_KEY', None).encode('utf-8'))
        m.update(os.urandom(16))
        otp = str(int(m.hexdigest(), 16))[-length:]
        return otp
