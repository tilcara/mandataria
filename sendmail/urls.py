from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'sendmail'

urlpatterns = [
    path('', home, name = 'home'),
    path('contact/', login_required(MailContact.as_view()), name = 'contact'),
]