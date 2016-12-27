from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
#from django.contrib.auth import views as auth_views

from website import views


urlpatterns = [
	#static.serve debe ser usado solo en dev environment Fuck!
	#url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
	url(r'^admin/', admin.site.urls),
	
	url(r'^$', views.index, name='home'),
	url(r'^empresa/', views.company, name='company'),
	url(r'^contacto/', views.contact, name='contact'),

	#url(r'^login/$', auth_views.login, {'template_name':'login.html'}, name='login'),
	url(r'^login/$', views.auth_login, name='login'),
	url(r'^extranet/', views.extranet, name='extranet'),
	url(r'^extranet/ctacte/', views.ctacte, name='ctacte'),

	url(r'^ctacte/', views.importcc, name='importcc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)