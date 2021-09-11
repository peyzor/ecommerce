from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

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
