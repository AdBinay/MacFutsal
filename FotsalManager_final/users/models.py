from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .utility import profile_img_path
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from core.abstract import CreateUpdatedModelMixin

class Batch(models.Model):
    name = models.CharField(_("Batch"),max_length=240)
    def __str__(self):return self.name
    
    
class Profile(CreateUpdatedModelMixin,models.Model):
    slug = models.SlugField(max_length=240,blank=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    image = models.ImageField(_("Avatar photo"), default="user/default/avtar.jpg", upload_to=profile_img_path)
    cover = models.ImageField(_("Cover photo"), default="user/default/cover.jpg", upload_to=profile_img_path)
    address = models.CharField(_("Address"), max_length=250,blank=True)
    current_ip = models.CharField(_("Current IP Address"),max_length=240,blank=True)
    batch = models.ForeignKey("Batch",on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):return self.user.get_full_name()
    
    def get_absolute_url(self):return reverse("profile", kwargs={"slug": self.slug})    
    def is_verified(self):return EmailAddress.objects.select_related('user').filter(user=self.user,verified=True).exists()    
    
    class Meta:
        verbose_name = _("Account Book")
