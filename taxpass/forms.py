from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Signup, Profile, Contact, Email


class SingupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('email', 'name', 'visa_status', 'occupation', 'marital_status', 'phone', 'state', 'callback_default', 'callback')


class UploadFileForm(forms.Form):
    file = forms.FileField()
    folder = forms.CharField(max_length=10)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email', 'company', 'address', 'city', 'state', 'phone', 'first_name', 'last_name', 'c_email', 'c_phone', 'navPosition', 'sidebarSize', 'colorScheme')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'phone', 'message')


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('contact',)