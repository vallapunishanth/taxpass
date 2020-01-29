from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from .forms import SingupForm, UploadFileForm, ProfileForm, ContactForm, EmailForm
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
                  'info@taxpas.com', ['info@taxpass.com'])
        redirect_context = {'inTheKnow': True, 'contact': s_form.cleaned_data['contact']}
        redirect_template = 'main/thankyou.html'
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
            callback_default = form.cleaned_data['callback_default']
            callback = form.cleaned_data['callback']
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            occupation = form.cleaned_data['occupation']
            marital_status = form.cleaned_data['marital_status']
            visa_status = form.cleaned_data['visa_status']
            state = form.cleaned_data['state']
            phone = form.cleaned_data['phone']
            services = ",".join([form.cleaned_data[str(i)] for i in range(1, 9) if str(i) in form.cleaned_data])
            obj, created = Signup.objects.update_or_create(
                email=email,
                name=name,
                marital_status=marital_status,
                occupation=occupation,
                visa_status=visa_status,
                state=state,
                phone=phone,
                services=services,
                callback_default=callback_default,
                callback=callback
            )

            if callback_default == '10-30 Mins':
                email_time = '10-30 Minutes'
            else:
                email_time = callback

            if created:
                update_info = False
                html_message = render_to_string('signup_email.html', {'name': name, 'time': email_time})
                send_mail('TaxPass Callback Confirmation',
                          'Hi {}! We have scheduled a callback in/on: {}'.format(name, email_time),
                          'Taxpass <info@taxpass.com>', [form.cleaned_data['email']], html_message=html_message)
                send_mail('Taxpass Signup - {}'.format(name), 'email: {}, phone: {}, company: {}, \
                time: {}, services: {}, '.format(email, phone, name, email_time, services), 'info@taxpass.com',
                          ['info@taxpass.com'])
            else:
                update_info = True

            if callback_default[0] == '10-30 Mins':
                time = True
            else:
                time = False
            redirect_context = {'email': form.cleaned_data['email'], 'update_info': update_info, 'time': time}
            redirect_template = 'thankyou.html'
            return render(request, redirect_template, redirect_context)
    else:
        form = SingupForm()
    context = {'signup_form': form, 'front_email': front_email}
    template = 'signup.html'
    return render(request, template, context)
#
#
# @login_required
# def portal(request):
#     template = 'main/portal.html'
#     context = {}
#     return render(request, template, context)
#
#
# password = None
#
#
# @login_required
# def new_customer(request):
#     global password
#     if password is None:
#         password = generate_password(8)
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['username']
#             form.save()
#             html_message = render_to_string('main/new_customer_email.html', {'email': email, 'password': password})
#
#             send_mail('Welcome to TrickyTax!', 'Your TrickyTax account has been created. \
#             Please login with the Email: {} and Password: {} using the link: https://trickytax.com/login \
#             '.format(email, password), 'TrickyTax <info@trickytax.com>', [email], html_message=html_message)
#
#             send_mail('TrickyTax New Customer - {}'.format(email), 'New customer has been created: {}'.format(email),
#                       'info@trickytax.com', ['info@trickytax.com'])
#             password = None
#             return redirect('/new_customer')
#     else:
#         form = UserCreationForm()
#     template = 'main/new_customer.html'
#     context = {'form': form, 'password': password}
#     return render(request, template, context)
#
#
# @login_required
# def documents(request):
#     if 'year' in request.GET:
#         year = request.GET['year']
#     else:
#         year = '2019'
#
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         folder = str(request.POST['folder'])
#         handle_uploaded_file(request.FILES['file'], request.user, year, folder)
#         url = '/documents?year=' + year
#         return redirect(url)
#     else:
#         form = UploadFileForm()
#     type1 = type2 = type3 = type4 = misc = None
#     try:
#         type1 = folder_list(request.user, year + '/Bookkeeping')
#         type2 = folder_list(request.user, year + '/Taxes')
#         type3 = folder_list(request.user, year + '/Payroll')
#         type4 = folder_list(request.user, year + '/Notices')
#         misc = folder_list(request.user, year + '/Misc')
#     except:
#         pass
#     return render(request, 'main/documents.html',
#                   {'upload_form': form, 'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'misc': misc,
#                    'year': year})  # add year here
#
#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('/profile')
#     else:
#         form = ProfileForm(instance=request.user.profile)
#     template = 'main/profile.html'
#     context = {'form': form}
#     return render(request, template, context)
#
#
# @login_required
# def get_file(request):
#     path = request.GET['path']
#     if request.user.username in path:
#         dbx_link = get_file_link(path)
#         return redirect(dbx_link)
#     return render(request, 'main/404.html')
#
#
# def about(request):
#     template = 'main/about.html'
#     return render(request, template)


def terms(request):
    template = 'terms.html'
    return render(request, template)
#
#
# def privacy(request):
#     template = 'main/privacy.html'
#     return render(request, template)
#
#
# def thankyou(request):
#     template = 'main/thankyou.html'
#     return render(request, template)
#
#
# def bookkeeping(request):
#     template = 'main/bookkeeping.html'
#     return render(request, template)
#
#
# def taxes(request):
#     template = 'main/taxes.html'
#     return render(request, template)
#
#
# def payroll(request):
#     template = 'main/payroll.html'
#     return render(request, template)
#
#
# def faq(request):
#     template = 'main/faq.html'
#     return render(request, template)
#
#
# @login_required
# def portal_v3(request):
#     if request.user.profile.password_changed == 'False':
#         return redirect('account')
#     template = 'main/dashkit/index.html'
#     navPosition, sidebarSize, colorScheme = request.user.profile.navPosition, request.user.profile.sidebarSize, request.user.profile.colorScheme
#     context = {'navPosition': navPosition, 'sidebarSize': sidebarSize, 'colorScheme': colorScheme}
#     return render(request, template, context)
#
#
# @login_required
# def document_vault(request):
#     if 'year' in request.GET:
#         year = request.GET['year']
#     else:
#         year = '2019'
#
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         folder = str(request.POST['folder'])
#         handle_uploaded_file(request.FILES['file'], request.user, year, folder)
#         url = '/document_vault?year=' + year
#         return redirect(url)
#     else:
#         form = UploadFileForm()
#     type1 = type2 = type3 = type4 = misc = None
#     try:
#         type1 = folder_list(request.user, year + '/Bookkeeping')
#         type2 = folder_list(request.user, year + '/Taxes')
#         type3 = folder_list(request.user, year + '/Payroll')
#         type4 = folder_list(request.user, year + '/Notices')
#         misc = folder_list(request.user, year + '/Misc')
#     except:
#         pass
#
#     file_counts = [len(type1), len(type2), len(type3), len(type3), len(type4), len(misc)]
#     navPosition, sidebarSize, colorScheme = request.user.profile.navPosition, request.user.profile.sidebarSize, request.user.profile.colorScheme
#     context = {'navPosition': navPosition, 'sidebarSize': sidebarSize, 'colorScheme': colorScheme, 'upload_form': form,
#                'type1': type1, 'type2': type2, 'type3': type3, 'type4': type4, 'misc': misc, 'year': year,
#                'file_counts': file_counts}
#     return render(request, 'main/dashkit/document_vault.html', context)
#
#
# @login_required
# def settings(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('/settings')
#     else:
#         form = ProfileForm(instance=request.user.profile)
#     template = 'main/dashkit/settings.html'
#     navPosition, sidebarSize, colorScheme = request.user.profile.navPosition, request.user.profile.sidebarSize, request.user.profile.colorScheme
#     context = {'navPosition': navPosition, 'sidebarSize': sidebarSize, 'colorScheme': colorScheme, 'form': form}
#     return render(request, template, context)
#
#
# @login_required
# def account(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             if request.user.profile.password_changed == 'False':
#                 profile = Profile.objects.get(email=request.user)
#                 profile.password_changed = 'True'
#                 profile.save()
#                 return redirect('/portal-v3')
#             return redirect('account')
#     else:
#         form = PasswordChangeForm(request.user)
#     template = 'main/dashkit/account.html'
#     navPosition, sidebarSize, colorScheme = request.user.profile.navPosition, request.user.profile.sidebarSize, request.user.profile.colorScheme
#     context = {'navPosition': navPosition, 'sidebarSize': sidebarSize, 'colorScheme': colorScheme, 'form': form}
#     return render(request, template, context)
#
#
# def contact(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             redirect_context = {'name': form.cleaned_data['name'], 'email': form.cleaned_data['email']}
#             redirect_template = 'main/thankyou.html'
#             send_mail('TrickyTax Contact Request', 'Name: {}, Email: {}, Subject: {}, Phone: {}, Message: {}' \
#                       .format(form.cleaned_data['name'], form.cleaned_data['email'],
#                               form.cleaned_data['subject'], form.cleaned_data['phone'],
#                               form.cleaned_data['message']), 'info@trickytax.com', ['info@trickytax.com'])
#             return render(request, redirect_template, redirect_context)
#     else:
#         form = ContactForm()
#     template = 'main/contact.html'
#     context = {'form': form}
#     return render(request, template, context)
#
#
# def error(request):
#     template = 'main/404.html'
#     return render(request, template)
#
#
# def referral(request):
#     template = 'main/referral.html'
#     return render(request, template)
#
#
#
#
#
# def chat(request):
#     template = 'main/chat.html'
#     return render(request, template)