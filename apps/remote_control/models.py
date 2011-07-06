"""
This module houses all of the DB models for the default player app. This
includes stuff like song request queues and histories.
"""
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import signals
from apps.music_player.managers import SongRequestManager
from libturpial.api.core import Core

PROTOCOLS=[]
for num, name in enumerate(Core().list_protocols()):
    PROTOCOLS.append((str(num),name))

PROTOCOLS = tuple(PROTOCOLS)

class Controller(models.Model):
    user = models.CharField(max_length=50,blank=True, null=True)
    password = models.CharField(max_length=50,blank=True, null=True)
    service = models.CharField(max_length=2,blank=True, null=True, choices=PROTOCOLS)


