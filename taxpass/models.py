from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.timezone import now


class Signup(models.Model):
    states = (
        ('', 'State'),
        ("Alabama","Alabama"),("Alaska","Alaska"),("Arizona","Arizona"),("Arkansas","Arkansas"),
        ("California","California"),("Colorado","Colorado"),("Connecticut","Connecticut"),
        ("Delaware","Delaware"),("Florida","Florida"),("Georgia","Georgia"),("Hawaii","Hawaii"),
        ("Idaho","Idaho"),("Illinois","Illinois"),("Indiana","Indiana"),("Iowa","Iowa"),
        ("Kansas","Kansas"),("Kentucky","Kentucky"),("Louisiana","Louisiana"),("Maine","Maine"),
        ("Maryland","Maryland"),("Massachusetts","Massachusetts"),("Michigan","Michigan"),
        ("Minnesota","Minnesota"),("Mississippi","Mississippi"),("Missouri","Missouri"),
        ("Montana","Montana"),("Nebraska","Nebraska"),("Nevada","Nevada"),("New Hampshire","New Hampshire"),
        ("New Jersey","New Jersey"),("New Mexico","New Mexico"),("New York","New York"),
        ("North Carolina","North Carolina"),("North Dakota","North Dakota"),("Ohio","Ohio"),
        ("Oklahoma","Oklahoma"),("Oregon","Oregon"),("Pennsylvania","Pennsylvania"),
        ("Rhode Island","Rhode Island"),("South Carolina","South Carolina"),
        ("South Dakota","South Dakota"),("Tennessee","Tennessee"),("Texas","Texas"),
        ("Utah","Utah"),("Vermont","Vermont"),("Virginia","Virginia"),("Washington","Washington"),
        ("West Virginia","West Virginia"),("Wisconsin","Wisconsin"),("Wyoming","Wyoming")
    )

    times = (
        ('', 'Callback Time'),
        ('10-30 Mins', '10-30 Minutes'),
        ('Later', 'Later'),
    )
    email = models.EmailField()
    name = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=50, blank=True)
    visa_status = models.CharField(max_length=50, blank=True)
    occupation = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=20, choices=states)
    phone = models.CharField(max_length=15)
    services = models.CharField(max_length=30)
    callback_default = models.CharField(max_length=20, choices=times)
    callback = models.CharField(max_length=30, blank=True)

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
