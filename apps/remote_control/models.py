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

    def __unicode__(self):
        return self.user


        print "%d. @%s: %s" % (count, status.username, text)
        print "%s from %s%s" % (status.datetime, status.source, inreply)
        if status.reposted_by:
            users = ''
            for u in status.reposted_by:
                users += u + ' '
            print 'Retweeted by %s' % status.reposted_by

class Tweet(models.Model):
    username = models.CharField(max_length=50,blank=True, null=True)
    text = models.CharField(max_length=256,blank=True, null=True)
    inreply = models.CharField(max_length=50,blank=True, null=True)
    source = models.CharField(max_length=50,blank=True, null=True)
    reposted = models.CharField(max_length=50,blank=True, null=True)
    datetime = models.CharField(max_length=100)

    def __unicode__(self):
        return self.text


