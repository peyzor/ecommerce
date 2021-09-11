from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User


@admin.action(description='Make selected users not active')
def make_users_not_active(modeladmin, request, queryset):
    queryset.update(is_active=False)


@admin.action(description='Make selected users verified')
def make_users_verified(modeladmin, request, queryset):
    queryset.update(is_verified=True)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'is_active', 'is_staff',
                  'is_verified')


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_staff', 'is_verified', 'is_active')
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'phone')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_verified', 'is_active')
        }),
    )

    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('email', 'username', 'password1', 'password2'),
    }), )
    search_fields = ('email', )
    ordering = ('email', )
    actions = (make_users_not_active, make_users_verified)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
