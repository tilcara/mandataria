from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.conf import settings

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


