from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email_verify'),
]
