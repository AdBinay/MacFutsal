from allauth.account.adapter import DefaultAccountAdapter
from .validators import is_email
from allauth.account.models import EmailAddress
class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        full_name = str(data.get("full_name"))
        batch = data.get("batch")
        
        f_name, *l_name = full_name.split(" ")
        user.first_name = f_name
        user.last_name = " ".join(l_name)

        user  = super(MyAccountAdapter, self).save_user(request, user, form, commit=True)
        
        if is_email(user.username) and user.profile:
            email , _ = EmailAddress.objects.get_or_create(user=user,email=user.username,primary=True)
            if email:
                email.send_confirmation(request=request,signup=True)

        user.profile.batch = batch
        user.profile.save()
        
        return user
