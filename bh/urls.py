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
	url(r'^lluvias-historico/$', views.historic_rain, name='historic_rain'),
	url(r'^impuestos/$', views.taxes, name='taxes'),
	url(r'^unidades-de-negocio/$', views.units, name='units'),
	url(r'^trabaja-con-nosotros/$', views.cv, name='cv'),

	url(r'^login/$', views.auth_login, name='login'),
	url(r'^login/invalido/$', views.auth_login_invalid, name='login_invalid'),
	url(r'^login/requerido/$', views.auth_login_required, name='login_required'),
	url(r'^login/cuenta-inactiva/$', views.auth_login_inactive_account, name='login_inactive_account'),
	url(r'^logout/$', views.auth_logout, name='logout'),
	url(r'^activar-cuenta/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.auth_activate_account, name='activate_account'),
	url(r'^cuenta/cambiar-password/$', views.change_password, name='change_password'),

	url(r'^extranet/$', views.extranet, name='extranet'),
	url(r'^extranet/notificaciones/$', views.notifications, name='notifications'),
	url(r'^extranet/ctacte/pesos/$', views.ctacte, name='ctacte'),
	url(r'^extranet/ctacte/aplicada/$', views.applied, name='applied'),
	url(r'^extranet/entregas/$', views.deliveries, name='deliveries'),
	url(r'^extranet/ventas/$', views.sales, name='sales'),

	url(r'^downloadexcel/rain/$', views.downloadRainExcel, name='download_rain'),
	url(r'^downloadexcel/(?P<module>[0-9A-Za-z_\-]+)/$', views.downloadexcel, name='downloadexcel'),
	url(r'^download/$', views.downloadPDFExtranet, name='downloadPDF'),

	url(r'^monedas/$', views.get_currency, name='currency'),
	url(r'^pizarras/$', views.get_board, name='board'),
	url(r'^lluvias/$', views.get_rain, name='rain'),

	url(r'^importar/(?P<datatype>[a-z]+)/$', views.importdata, name='importdata'),

	url(r'^400/$', views.handler404, name='handler400'),
	url(r'^404/$', views.handler404, name='handler404'),
	url(r'^500/$', views.handler500, name='handler500'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'website.views.handler404'
handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'