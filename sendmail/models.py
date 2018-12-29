from django.db import models
from django.contrib.auth.models import User

class Mail(models.Model):
	user = models.ForeignKey(User, null = True, blank = True, on_delete = models.CASCADE)
	subject = models.CharField(max_length = 32)
	message = models.TextField()
	def __str__(self):
		return self.subject 