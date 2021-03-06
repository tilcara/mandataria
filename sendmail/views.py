from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from .forms import MailForm
from .models import Mail

import requests
import json

@login_required
def home(request):
    social_user = request.user.social_auth.filter(provider='facebook').first()
    if social_user :
        url = 'https://graph.facebook.com/{0}/?fields=id,name,email&access_token={1}'.format(social_user.uid, social_user.extra_data['access_token'],)
        user_json = requests.get(url).json()
        user_name = json.dumps(user_json['name'],ensure_ascii=False)
        request.user.username = user_name
        request.user.save()
        try:
            user_email = json.dumps(user_json['email'])
            request.user.email = user_email
            request.user.save()
        except:
            request.user.email = ""
            request.user.save()
    setattr(request, 'view', 'sendmail.views.home')
    return render(request, 'sendmail/home.html')

@login_required
def services(request):
	setattr(request, 'view', 'sendmail.views.services')
	return render(request, 'sendmail/services.html')


class MailContact(CreateView):
	model = Mail
	form_class = MailForm
	template_name = 'sendmail/mail-contact.html'
	success_url = reverse_lazy('sendmail:home')
	def post(self,request,*args,**kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			current_user = request.user
			mail = form.save(commit=False)
			mail.user = current_user
			mail.save()
			email_from = mail.user.username
			email = mail.user.email
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message'] + '\n' +' de: '+ email_from +' '+ email
			recipient_list = [settings.EMAIL_HOST_USER]
			send_mail(subject, message, email_from, recipient_list)
			return HttpResponseRedirect(self.get_success_url())

		else:
			return render(request, self.template_name, {'form':form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Revisa tu email, te enviamos un link, dale click para verificar tu cuenta :)')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f'Gracias {user.username} por registrarse!')
        return redirect('sendmail:home')
    else:
        return HttpResponse('El link es invalido!')