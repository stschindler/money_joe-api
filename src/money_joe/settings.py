import environ

import os

env = environ.Env()
env.read_env(".env")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = env("MJOE_DEBUG", default=False)
SECRET_KEY = env("MJOE_SECRET_KEY")
ALLOWED_HOSTS = env.list("MJOE_ALLOWED_HOSTS", default=["*"])
STATIC_URL = env("MJOE_STATIC_URL", default="/static/")
STATIC_ROOT = env.path("MJOE_STATIC_ROOT", default="public/static")
MEDIA_URL = env("MJOE_MEDIA_URL", default="/media/")
MEDIA_ROOT = env.path("MJOE_MEDIA_ROOT", default="public/media")

DATABASES = {"default": env.db("MJOE_DATABASE")}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
ROOT_URLCONF = "money_joe.urls"
WSGI_APPLICATION = "money_joe.wsgi.application"

INSTALLED_APPS = [
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",

  "household",
  "tag",
  "account",
  "journal",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
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
