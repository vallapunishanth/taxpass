from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.timezone import now


class Signup(models.Model):

    email = models.EmailField()
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)
    utc_callback = models.DateTimeField(null=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    # Business Info
    email = models.OneToOneField(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    occupation = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    # Point of Contact
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    c_email = models.CharField(max_length=50, blank=True)
    c_phone = models.CharField(max_length=30, blank=True)

    # Vault Settings
    navPosition = models.CharField(max_length=30, default='sidenav')
    sidebarSize = models.CharField(max_length=30, default='base')
    colorScheme = models.CharField(max_length=30, default='light')

    # Password Change
    password_changed = models.CharField(max_length=10, default='False')

    def __str__(self):
        return '{}\'s Profile'.format(self.email)


class Contact(models.Model):

    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    message = models.TextField(max_length=1000)

    def __str__(self):
        return self.name


class Email(models.Model):
    contact = models.EmailField(max_length=50)

    def __str__(self):
        return str(self.contact)
