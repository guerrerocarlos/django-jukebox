"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from apps.remote_control.models import Controller

admin.site.register(Controller)
