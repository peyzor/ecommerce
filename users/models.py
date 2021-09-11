from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


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
        # Add db table later
        # db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')
