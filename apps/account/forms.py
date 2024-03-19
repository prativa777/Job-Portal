from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from apps.account.models import UserProfile

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'first_name',
                  'middle_name', 'last_name']


class UserLoginForm(forms.Form):
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', "profile_picture", "phone_number", "address", "resume"]

    def clean_profile_picture(self):
        pp = self.cleaned_data.get('profile_picture')
        if pp:
            extension = pp.name.split(".")[-1]  # picture.jpg  = ["picture", "jpg"]
            if extension.lower() not in ['jpg', 'png', "jpeg", 'svg']:
                raise ValidationError("Profile Picture Must Be In Image Format !!")
        return pp

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            extension = resume.name.split(".")[-1]
            if extension.lower() not in ['pdf', 'docx']:
                raise ValidationError("Resume must be a pdf or a docx file !!")
        return resume