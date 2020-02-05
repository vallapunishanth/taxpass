from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from .forms import SingupForm, EmailForm
import datetime
from taxpass import settings
from .models import Signup, Profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
# from .handlers import handle_uploaded_file, folder_list, get_file_link, generate_password
from django.template import Context


def home(request):
    s_form = EmailForm()
    context = {'s_form': s_form}
    template = 'home.html'
    if request.method == 'POST' and 'contact' in request.POST:
        s_form = EmailForm(request.POST)
        s_form.save()
        send_mail('Taxpass New Email',
                  'New email through In The Know Section: {}'.format(s_form.cleaned_data['contact']),
                  settings.EMAIL_HOST, [settings.EMAIL_HOST])
        redirect_context = {'inTheKnow': True, 'contact': s_form.cleaned_data['contact']}
        redirect_template = 'thankyou.html'
        return render(request, redirect_template, redirect_context)
    elif request.method == 'POST':
        email = request.POST.get('email')
        template = 'signup?email={}'.format(email)
        return redirect(template)
    else:
        return render(request, template, context)


def signup(request):
    if 'email' in request.GET:
        front_email = request.GET['email']
    else:
        front_email = ''
    if request.method == 'POST':
        form = SingupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            utc_callback = form.cleaned_data['utc_callback']
            print(utc_callback.strftime("%m-%d-%Y %H:%M %Z%z"))
            obj, created = Signup.objects.update_or_create(
                email=email,
                name=name,
                phone=phone,
                utc_callback=utc_callback
            )

            if created:
                update_info = False
                html_message = render_to_string('signup_email.html', {'name': name, 'time': utc_callback.strftime("%m-%d-%Y %H:%M %Z%z")})
                send_mail('TaxPass Callback Confirmation',
                          'Hi {}! We have scheduled a callback in/on: {}'.format(name, utc_callback),
                          settings.EMAIL_HOST, [form.cleaned_data['email']], html_message=html_message)
                send_mail('Taxpass Signup - {}'.format(name), 'email: {}, phone: {}, company: {}, \
                time: {}'.format(email, phone, name, utc_callback), settings.EMAIL_HOST,
                          [settings.EMAIL_HOST])
            else:
                update_info = True

            time = False
            redirect_context = {'email': form.cleaned_data['email'], 'update_info': update_info, 'time': time}
            redirect_template = 'thankyou.html'
            return render(request, redirect_template, redirect_context)
    else:
        form = SingupForm()
    context = {'signup_form': form, 'front_email': front_email, 'form': form}
    template = 'signup.html'
    return render(request, template, context)


def terms(request):
    template = 'terms.html'
    return render(request, template)
