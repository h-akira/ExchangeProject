from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-{}'
# 以下の手順で生成する
# python3 manage.py shell
# from django.core.management.utils import get_random_secret_key
# get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# 本番環境ではFalseにする

# 配信するドメインやIP
ALLOWED_HOSTS = []
# PythonAnuwhereの無料プランの場合は
# ALLOWED_HOSTS = ["<username>.pythonanywhere.com"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

# サインアップの可否
SIGNUP = True

