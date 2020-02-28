from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import SingupForm, EmailForm
from taxpass import settings
from .models import Signup
from django.core.mail import send_mail
from datetime import datetime
from django.template.loader import render_to_string


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
            actual_time = request.POST['actual_time']
            # print(utc_callback.strftime("%m-%d-%Y %H:%M %Z%z"))
            client_time = datetime.strptime(actual_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            # print(client_time)
            # obj, created = Signup.objects.update_or_create(
            #     email=email,
            #     name=name,
            #     phone=phone,
            #     utc_callback=utc_callback
            # )
            obj, created = None, True
            if created:
                update_info = False
                html_message = render_to_string('signup_email.html', {'name': name, 'time': client_time.strftime("%m-%d-%Y %H:%M %Z%z")})
                send_mail('TaxPass Callback Confirmation',
                          'Hi {}! We have scheduled a callback in/on: {}'.format(name, utc_callback),
                          settings.EMAIL_HOST, [form.cleaned_data['email']], html_message=html_message)
                send_mail('Taxpass Signup - {}'.format(name), 'email: {}, phone: {}, company: {}, \
                time: {}'.format(email, phone, name, utc_callback.strftime("%m-%d-%Y %H:%M %Z%z")), settings.EMAIL_HOST,
                          [settings.EMAIL_HOST])
            else:
                update_info = True

            time = False
            redirect_context = {'email': form.cleaned_data['email'], 'update_info': update_info, 'time': time}
            redirect_template = 'thankyou.html'
            return render(request, redirect_template, redirect_context)
        else:
            print("Form is invalid")
            form = SingupForm()

    else:
        form = SingupForm()
    context = {'signup_form': form, 'front_email': front_email, 'form': form}
    template = 'signup.html'
    return render(request, template, context)


def terms(request):
    template = 'terms.html'
    return render(request, template)


def about(request):
    template = 'about.html'
    return render(request, template)