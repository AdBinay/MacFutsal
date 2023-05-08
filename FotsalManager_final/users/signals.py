from django.db.models import signals
from django.dispatch import receiver
from django.utils.text import slugify
from django.conf import settings
from allauth.account.models import EmailAddress
from .validators import is_email
from .models import Profile
from django.contrib.auth.models import User

SIGNATURE = getattr(settings,"SIGNATURE")
  
@receiver(signals.pre_save, sender=User)
def pre_usersave(sender, instance, **kwargs):
    if is_email(instance.username):
        instance.email = instance.username
    if instance.is_superuser:
        if not instance.first_name:
            instance.first_name = "Sharad"
            instance.last_name = "Bhandari"

@receiver(signals.post_save, sender=User)
def post_usersave(sender, created, instance, **kwargs):
    if created:
        if is_email(instance.username):
            EmailAddress.objects.get_or_create(user=instance,email=instance.username,primary=True)
        if not Profile.objects.filter(user=instance).exists():
            full_name = " ".join([instance.first_name, instance.last_name])
            user_id = instance.id
            user_slug = slugify(value=str(full_name + " " + str(user_id)))
            Profile.objects.create(user=instance, slug=user_slug)