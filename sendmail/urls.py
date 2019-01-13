from django.urls import path, re_path
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'sendmail'

urlpatterns = [
    path('', home, name = 'home'),
    path('contact/', login_required(MailContact.as_view()), name = 'contact'),
    path('services/', services, name = 'services'),
    path('signup/', signup, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate')
]				