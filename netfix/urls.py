from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from . import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('services/', include('services.urls')),
    path('register/', include('users.urls')),
  
    path('customer/<slug:name>', v.customer_profile, name='customer_profile'),
    path('company/<slug:name>', v.company_profile, name='company_profile'),
    path('services/company/<slug:name>', v.company_profile, name='company_profile')
]
