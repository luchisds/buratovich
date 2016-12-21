from django.conf.urls import url
from django.contrib import admin

from website import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='home'),
	url(r'^empresa/', views.company, name='company'),
	url(r'^contacto/', views.contact, name='contact'),
]
