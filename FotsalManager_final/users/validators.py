from django import forms
from allauth.account.models import EmailAddress
from django.db.models import Q
from django.contrib.auth.models import User
import re 
from PIL import Image

def is_email(email):
    EMAIL_REGEX = r"^[A-z\d\.\+]+@[\w\d]+\.[a-z]+"    
    return True if re.match(EMAIL_REGEX, email) is not None else False

def UsernameValidator(username):
    if is_email(username) is not True:
        raise forms.ValidationError(message="Email is in Invalid Format.")
    if any(
        [
            User.objects.filter(Q(username=username) | Q(email=username)).exists(),
            EmailAddress.objects.select_related('user').filter(email=username).exists(),
        ]
    ):
        raise forms.ValidationError(
            message="This username has already been assigned or in use."
        )
    return username

username_validator = [UsernameValidator]

def check_img(image_file):
    try:
        image_file.seek(0)
        im = Image.open(image_file)
        im.verify()
        im.close()
        image_file.seek(0)
        im = Image.open(image_file)
        im.transpose(Image.FLIP_LEFT_RIGHT)
        im.close()
        return True
    except:
        return None