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
	url(r'^historico_lluvias/$', views.historic_rain, name='historic_rain'),
	url(r'^impuestos/$', views.taxes, name='taxes'),

	url(r'^login/$', views.auth_login, name='login'),
	url(r'^login/invalid/$', views.auth_login_invalid, name='login_invalid'),
	url(r'^login/required/$', views.auth_login_required, name='login_required'),
	url(r'^login/inactive_account/$', views.auth_login_inactive_account, name='login_inactive_account'),
	url(r'^logout/$', views.auth_logout, name='logout'),
	url(r'^activate_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.auth_activate_account, name='activate_account'),
	url(r'^account/change_password/$', views.change_password, name='change_password'),

	url(r'^extranet/$', views.extranet, name='extranet'),
	url(r'^extranet/notifications/$', views.notifications, name='notifications'),
	url(r'^extranet/ctacte/pesos/$', views.ctacte, name='ctacte'),
	url(r'^extranet/ctacte/applied/$', views.applied, name='applied'),
	url(r'^extranet/deliveries/$', views.deliveries, name='deliveries'),
	url(r'^extranet/sales/$', views.sales, name='sales'),

	url(r'^downloadexcel/(?P<module>[0-9A-Za-z_\-]+)/$', views.downloadexcel, name='downloadexcel'),

	url(r'^currency/$', views.get_currency, name='currency'),
	url(r'^board/$', views.get_board, name='board'),
	url(r'^rain/$', views.get_rain, name='rain'),

	url(r'^import/(?P<datatype>[a-z]+)/$', views.importdata, name='importdata'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)