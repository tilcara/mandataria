from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Mail


class MailForm(forms.ModelForm):
	class Meta:
		model = Mail
		fields = [
			'user',
			'subject',
			'message',
		]
		labels = {
			'subject' : 'Asunto',
			'message' : 'Consulta',
		}
		widgets = {
			'subject': forms.TextInput(attrs={'class':'form-control'}),
			'message': forms.Textarea(attrs={'class':'form-control'}),
		}

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')