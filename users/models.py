from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    phone_number_validator = RegexValidator(r'^(\+98|0)?9\d{9}$',
                                            message=_('wrong number'))

    user = models.OneToOneField(User,
                                verbose_name=_('user'),
                                on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(_('age'), blank=True, null=True)
    photo = models.ImageField(_('photo'),
                              upload_to='users',
                              blank=True,
                              null=True)
    phone_number = models.PositiveBigIntegerField(
        _('phone number'),
        unique=True,
        blank=True,
        null=True,
        validators=[phone_number_validator])
    bio = models.TextField(_('bio'), max_length=300, blank=True)

    class Meta:
        db_table = 'profile'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user.username


# signals to create profile after a user is created


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
