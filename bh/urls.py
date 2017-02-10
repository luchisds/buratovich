from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin

from website import views


urlpatterns = [
	# static.serve debe ser usado solo en dev environment Fuck!
	# url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),

	# Django-admin-tools URL's
	url(r'^admin_tools/', include('admin_tools.urls')),

	url(r'^admin/', admin.site.urls),
	
	url(r'^$', views.index, name='home'),
	url(r'^empresa/$', views.company, name='company'),
	url(r'^contacto/$', views.contact, name='contact'),

	url(r'^login/$', views.auth_login, name='login'),
	url(r'^login/invalid/$', views.auth_login_invalid, name='login_invalid'),
	url(r'^login/required/$', views.auth_login_required, name='login_required'),
	url(r'^logout/$', views.auth_logout, name='logout'),
	url(r'^extranet/$', views.extranet, name='extranet'),
	url(r'^extranet/notifications/$', views.notifications, name='notifications'),
	url(r'^extranet/ctacte/pesos/$', views.ctacte, name='ctacte'),
	url(r'^extranet/ctacte/kilos/$', views.ctactekg, name='ctactekg'),
	url(r'^extranet/sales/$', views.sales, name='sales'),

	url(r'^extranet/ctacte/downloadexcel/$', views.downloadexcel, name='downloadexcel'),
	url(r'^extranet/ctacte/downloadtxt/$', views.downloadtxt, name='downloadtxt'),

	url(r'^import/(?P<typecc>[a-z]+)/$', views.importdata, name='importdata'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)