from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Signup, Profile, Contact, Email
# from bootstrap_datepicker_plus import DatePickerInput


class SingupForm(forms.ModelForm):
    class Meta:
        model = Signup
        fields = ('email', 'name', 'phone', 'utc_callback')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('email', 'company', 'address', 'city', 'phone', 'first_name', 'last_name', 'c_email', 'c_phone', 'navPosition', 'sidebarSize', 'colorScheme')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'phone', 'message')


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('contact',)