"""
Admin interface models. Automatically detected by admin.autodiscover().
"""
from django.contrib import admin
from apps.remote_control.models import Controller, Tweet

admin.site.register(Controller)
admin.site.register(Tweet)
