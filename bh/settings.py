import os
from datetime import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(BASE_DIR+'/bh/secret_key.txt') as f:
	SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*','127.0.0.1', 'buratovich.herokuapp.com']


# Application definition

INSTALLED_APPS = [
	'django.contrib.contenttypes',
	#'jet',
	'grappelli.dashboard',
	'grappelli',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.humanize',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'website',
	'el_pagination',
	'mathfilters',
	# 'admin_reorder',
]

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# 'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'bh.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [],
		# When using loaders APP_DIRS must be commented
		#'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
			'loaders': [
				# When using loaders it is necessary to indicate the templates loaders for Django (filesystem and apps)
				('django.template.loaders.cached.Loader', [
				'django.template.loaders.filesystem.Loader',
				'django.template.loaders.app_directories.Loader',
				]),
			],
		},
	},
]

WSGI_APPLICATION = 'bh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

# DATABASES = {
# 	'default': {
# 		'ENGINE': 'django.db.backends.postgresql',
# 		'NAME': 'buratovich',
# 		'USER': 'postgres',
# 		'PASSWORD': 'luciano',
# 		'HOST': 'localhost',
# 		'PORT': '5432',
# 	}
# }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Buenos_Aires'

USE_I18N = True

USE_L10N = True

# This work if USE_L10N is set to True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
DECIMAL_SEPARATOR = ','

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_DIRS = [
	('ctacte', os.path.join(BASE_DIR, 'FTP', 'CtaCtePesos')),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


# Custom User model
# AUTH_USER_MODEL = 'website.User'


FILE_UPLOAD_HANDLERS = (
	# Django-excel
	'django_excel.ExcelMemoryFileUploadHandler',
	'django_excel.TemporaryExcelFileUploadHandler',
	# Django
	# 'django.core.files.uploadhandler.MemoryFileUploadHandler',
	# 'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)


# Redirect to this URL when try to access unauthorized user to extranet URL
LOGIN_URL = '/login/requerido/'

# Redirect this URL on login
LOGIN_REDIRECT_URL = '/extranet/'

# Django El Pagination
EL_PAGINATION_PER_PAGE = 50

# Jeet Settings
# JET_DEFAULT_THEME = 'light-green'
# JET_THEMES = ''
# JET_SIDE_MENU_COMPACT = True
# JET_SIDE_MENU_CUSTOM_APPS = [
# 	('auth', [
# 		'User',
# 	]),
# 	('website', [
# 		'Currencies',
# 		'Board',
# 		'Rain',
# 		'City',
# 		'CtaCte',
# 		'Notifications',
# 		'ViewedNotifications',
# 	]),
# ]

# Grappelli Settings
GRAPPELLI_ADMIN_TITLE = 'BURATOVICH HNOS.'
GRAPPELLI_INDEX_DASHBOARD = 'website.dashboard.CustomIndexDashboard'

# Admin Reorder Settings
# ADMIN_REORDER = (
# 	{'app': 'auth', 'label': 'Alta de Usuarios'},
# 	{'app': 'website', 'label': 'Moneda y Pizarra', 'models': ('website.Currencies', 'website.Board')},
# 	{'app': 'website', 'label': 'Lluvias', 'models': ('website.Rain', 'website.City')},
# 	{'app': 'website', 'label': 'Notificaciones', 'models': ('website.Notifications', 'website.ViewedNotifications')},
# )

# CP Online settings
CP_CONTENT_TYPES = ['application/pdf',]
CP_MAX_UPLOAD_SIZE = 2621440 #2.5 Mb

# EMAIL Configuration
with open(BASE_DIR+'/bh/email_account.txt') as f:
	ea = f.read().strip().split(':')
	EMAIL_HOST = ea[0]
	EMAIL_HOST_PASSWORD = ea[3]
	EMAIL_HOST_USER = ea[2]
	EMAIL_PORT = ea[1]


# REMOTE SERVER
with open(BASE_DIR+'/bh/remote_server.txt') as f:
	rs = f.read().strip().split(':')
	RS_USER = rs[0]
	RS_PASS = rs[1]