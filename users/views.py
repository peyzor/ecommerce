import jwt
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer
from .models import User
from .utils import Util


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email_verify')
        absolute_url = f'https://{current_site}{relative_link}?token={token}'

        email_body = f'Hi {user.username}. Please use the link below to verify your email\n{absolute_url}'
        email_data = {
            'subject': 'Verify your email',
            'body': email_body,
            'to': user.email
        }
        Util.send_email(email_data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerifyView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = jwt.decode(token,
                                 settings.SECRET_KEY,
                                 algorithms=['HS256'])

            user = User.objects.get(pk=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'email': "Successfully activated"},
                            status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation expired'},
                            status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
