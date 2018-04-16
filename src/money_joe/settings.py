import environ

import base64
import os

env = environ.Env()
env_path = env("MJOE_ENV_PATH", default=".env")
env.read_env(env_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = env("MJOE_DEBUG", default=False)
SECRET_KEY = env("MJOE_SECRET_KEY")
ALLOWED_HOSTS = env.list("MJOE_ALLOWED_HOSTS", default=["*"])

PROTOCOL = env("MJOE_PROTOCOL", default="https")
CDN_ENDPOINT = env("MJOE_CDN_ENDPOINT", default="cdn.moneyjoe.io")
API_ENDPOINT = env("MJOE_API_ENDPOINT", default="api.moneyjoe.io")
WEB_ENDPOINT = env("MJOE_WEB_ENDPOINT", default="app.moneyjoe.io")
CDN_ROOT_PATH = env("MJOE_CDN_ROOT_PATH", default="/opt/moneyjoe")

STATIC_URL = env(
  "MJOE_STATIC_URL", default="{}://{}/static/".format(PROTOCOL, CDN_ENDPOINT)
)
STATIC_ROOT = \
  env("MJOE_STATIC_ROOT", default="{}/static".format(CDN_ROOT_PATH))

MEDIA_URL = env(
  "MJOE_MEDIA_URL",
  default="{}://{}/media/".format(PROTOCOL, CDN_ENDPOINT),
)
MEDIA_ROOT = env("MJOE_MEDIA_ROOT", default="{}/media".format(CDN_ROOT_PATH))

CDN_URL = \
  env("MJOE_CDN_URL", default="{}://{}".format(PROTOCOL, CDN_ENDPOINT))
API_URL = \
  env("MJOE_API_URL", default="{}://{}".format(PROTOCOL, API_ENDPOINT))
WEB_URL = \
  env("MJOE_WEB_URL", default="{}://{}".format(PROTOCOL, WEB_ENDPOINT))

DATABASES = {"default": env.db("MJOE_DATABASE")}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
ROOT_URLCONF = "money_joe.urls"
WSGI_APPLICATION = "money_joe.wsgi.application"

EMAIL_HOST = env("MJOE_EMAIL_HOST", default="localhost")
EMAIL_PORT = int(env("MJOE_EMAIL_PORT", default=587))
EMAIL_HOST_USER = env("MJOE_EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("MJOE_EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("MJOE_EMAIL_USE_TLS", default=True)
EMAIL_SUBJECT_PREFIX = \
  env("MJOE_EMAIL_SUBJECT_PREFIX", default="[MoneyJoe] ")
EMAIL_FROM_ADDRESS = env("MJOE_EMAIL_FROM_ADDRESS", default="hi@moneyjoe.io")

INSTALLED_APPS = [
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",

  "graphene",
  "graphene_django",

  "joetils",
  "layout",
  "geo",
  "user_profile",
  "mail",
  "registration",
  "currency",
  "household",
  "tag",
  "account",
  "journal",
  "graphql_api",
  "demodata",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",

  "graphql_api.middleware.AuthTokenMiddleware",
]

TEMPLATES = [
  {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {
      "context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
      ],
    },
  },
]

AUTH_PASSWORD_VALIDATORS = [
  {"NAME": "django.contrib.auth.password_validation.{}".format(module)}
  for module in (
    "UserAttributeSimilarityValidator", "MinimumLengthValidator",
    "CommonPasswordValidator", "NumericPasswordValidator",
  )
]
