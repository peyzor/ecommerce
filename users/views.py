from django.views import generic
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Profile


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('products:home')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


class LoginView(auth_views.LoginView):
    template_name = 'registration/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'registration/logout.html'


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/user_password_reset_form.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'registration/user_password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/user_password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'registration/user_password_reset_complete.html'


class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
    context_object_name = 'profile'

    def get_queryset(self, *args, **kwargs):
        """ only the current user can see its own profile """
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(pk=self.request.user.profile.pk)


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    fields = ('age', 'photo', 'phone_number', 'bio')
    template_name = 'users/profile_update.html'

    def get_queryset(self, *args, **kwargs):
        """ only the current user can update its own profile """
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(pk=self.request.user.profile.pk)
