from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password_reset/',
         views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/',
         views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/',
         views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('profile-detail/<int:pk>/',
         views.ProfileDetailView.as_view(),
         name='profile_detail'),
    path('profile-update/<int:pk>/',
         views.ProfileUpdateView.as_view(),
         name='profile_update'),
]
