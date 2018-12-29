from django import forms
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