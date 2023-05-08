from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth import get_user_model
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.models import EmailAddress
from django.db.models import Q
import io

from .adapters import MyAccountAdapter
from .models import Profile,Batch
from .validators import UsernameValidator
from .validators import is_email,check_img

User = get_user_model()

class LogInForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LogInForm, self).__init__(*args, **kwargs)
        self.fields["login"].label = _("Email or Username")
        self.fields["password"].widget = forms.PasswordInput()
        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = ""

class SignUpForm(SignupForm):
    full_name = forms.CharField(label=_("Full Name"),max_length=100)
    email = forms.EmailField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(label=_("Email or Username"),min_length=5,max_length=200,required=True,validators=[UsernameValidator])
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),required=True)
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Email or Username"
        for field in self.fields:
            self.fields[field].widget.attrs["placeholder"] = ""

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UsernameValidator(username=username):
            return username
        return forms.ValidationError("Please provide valid username")
    
    def save(self, request):
        adapter = MyAccountAdapter(request)
        user = adapter.new_user(request)
        return adapter.save_user(request, user, self)

class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(label="Full Name", min_length=5,max_length=100, required=True)
    email = forms.EmailField(label="Email",widget=forms.EmailInput(),max_length=100, required=False)
    batch = forms.ModelChoiceField(queryset=Batch.objects.all(),required=True)
    
    def __init__(self,*args, **kwargs):
        self.user = kwargs.pop('user', None)
        print("Profile Update user :",self.user)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['full_name'].initial = self.user.get_full_name() or ''
            primary_email = EmailAddress.objects.filter(user=self.user,primary=True).first() or ''
            self.fields['email'].initial = primary_email 
            
    def clean_full_name(self):
        fname,*lname = str(self.cleaned_data.get('full_name')).strip().split(" ")
        lname = " ".join(lname)
        self.user.first_name = fname
        self.user.last_name = lname
        self.user.save()

    def clean_email(self):
        email_qs_user = EmailAddress.objects.filter(user=self.user)
        email_address = self.cleaned_data.get('email')
        if email_address:
            email_qs = EmailAddress.objects.exclude(user=self.user).filter(email=email_address)
            user_qs = User.objects.exclude(username=self.user.username).filter(Q(username=email_address))

            # Other user using check
            if any([email_qs.exists(),user_qs.exists()]):
                raise forms.ValidationError('This email is already in use.')
            # Format Check
            if not is_email(email_address):
                raise forms.ValidationError('Email format is invalid.')
            # Already exist for this user check
            verified = False
            if email_qs_user.exists():
                for email in email_qs_user:
                    if email.verified:
                        verified = True 
                    email.delete()
            if is_email(email_address):
                EmailAddress.objects.get_or_create(user=self.user,email=email_address,primary=True,verified=verified)
            return email_address
        email_qs_user.delete()
        return ''
    
    def clean_image(self):
        return self.clean_any_image('image')

    def clean_cover(self):
        return self.clean_any_image('cover')

    def clean_any_image(self, field_name):
        image = self.cleaned_data.get(field_name)
        if image:
            with io.BytesIO(image.read()) as image_file:
                if check_img(image_file):
                    return image
                else:
                    raise forms.ValidationError('Valid Image file is required.')
        else:
            raise forms.ValidationError('This Image field is required.')
    
    class Meta:
        model = Profile
        fields = ["image","cover","full_name","address","batch","email"]
        