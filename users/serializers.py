from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_str, smart_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User, PhoneToken
from .utils import Util


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=70,
                                     min_length=6,
                                     write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                _('The username should only contain alphanumeric characters'))
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255,
                                   min_length=4,
                                   required=False)
    password = serializers.CharField(max_length=60,
                                     min_length=6,
                                     write_only=True)
    phone = serializers.CharField(allow_blank=True,
                                  allow_null=True,
                                  max_length=128,
                                  required=False)
    username = serializers.SerializerMethodField()
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'phone', 'password', 'username', 'tokens']

    def get_tokens(self, obj):
        email = obj.get('email')
        phone = obj.get('phone')
        try:
            user = User.objects.get(Q(email=email) | Q(phone=phone))
            return user.tokens()

        except User.DoesNotExist:
            return None

    def get_username(self, obj):
        email = obj.get('email')
        phone = obj.get('phone')
        try:
            user = User.objects.get(Q(email=email) | Q(phone=phone))
            return user.username

        except User.DoesNotExist:
            return None

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        phone = attrs.get('phone')

        user = authenticate(email=email, phone=phone, password=password)

        if not user:
            raise AuthenticationFailed(_('Invalid credentials, try again'))

        if not user.is_active:
            raise AuthenticationFailed(_('Account disabled'))

        if not user.is_verified:
            raise AuthenticationFailed(_('Email is not verified'))

        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, min_length=4)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(self.context.get('request')).domain
            relative_link = reverse('users:password_reset_confirm',
                                    kwargs={
                                        'uidb64': uidb64,
                                        'token': token
                                    })
            absolute_url = f'http://{current_site}{relative_link}'

            email_body = f'Hello, Please use the link below to verify your email\n{absolute_url}'
            email_data = {
                'subject': 'Reset your password',
                'body': email_body,
                'to': user.email
            }

            Util.send_email(email_data)

        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,
                                     max_length=60,
                                     write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(_('The reset link is invalid'), 401)

            user.set_password(password)
            user.save()

        except Exception:
            raise AuthenticationFailed(_('The reset link is invalid'), 401)

        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(min_length=1)

    def validate(self, attrs):
        self.token = attrs.get('refresh')

        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad token')


class PhoneTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneToken
        fields = ['pk', 'phone']


class PhoneTokenUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PhoneTokenValidateSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=40)

    class Meta:
        model = PhoneToken
        fields = ['pk', 'otp']
