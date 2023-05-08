from typing import Any, Dict
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from . import models,forms
from futsal import models as futsal_models
class RedirectUserProfile(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return self.request.user.profile.get_absolute_url()

class AccountDetailView(LoginRequiredMixin,generic.DetailView):
    model = models.Profile
    slug_field = "slug"
    context_object_name = "profile"
    slug_url_kwarg = "slug"
    template_name = 'pages/profile.html'

    def get_context_data(self, **kwargs):
        profile = self.get_object()
        context = super().get_context_data(**kwargs)
        context["match_played"] = futsal_models.Players.objects.filter(player=profile.user,match__completed=True).count()
        context["played_games"] = futsal_models.Players.objects.filter(player=profile.user,match__completed=True)
        context["user_score_count"] = futsal_models.Players.objects.filter(player=profile.user).aggregate(models.models.Sum('score'))['score__sum']
        return context
    
class UpdateProfile(LoginRequiredMixin,generic.UpdateView):
    model = models.Profile
    form_class = forms.UserProfileForm
    template_name = "forms/profile_update_form.html"
    

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
    def get_object(self, queryset=None):
        return get_object_or_404(self.model,user=self.request.user)
    
    def get_success_url(self):
        return reverse("redirect_profile")