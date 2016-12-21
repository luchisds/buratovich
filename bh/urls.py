from django.conf.urls import url
from django.contrib import admin

from website import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	#static.serve debe ser usado solo en dev environment Fuck!
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.index, name='home'),
	url(r'^empresa/', views.company, name='company'),
	url(r'^contacto/', views.contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)