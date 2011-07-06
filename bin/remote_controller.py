#!/usr/bin/env python
"""
Retrieve Controllers (tweets and dents) messages and handles them properly \
into processing of commands embeded into messages
"""
import sys
import os
# Setup the Django environment
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
# Back to the ordinary imports
from django.conf import settings
from apps.remote_control.models import Controller, Tweet
from libturpial.api.core import Core
from libturpial.common import clean_bytecodes, ColumnType

def process_statuses(statuses):
    if statuses.code > 0:
        print statuses.errmsg
        return

    count = 1

    for status in statuses[::-1]:
        text = status.text.replace('\n', ' ')
        inreply = ''
        if status.in_reply_to_user:
            inreply = ' en respuesta a %s' % status.in_reply_to_user
        print "%d. @%s: %s" % (count, status.username, text)
        print "%s from %s%s" % (status.datetime, status.source, inreply)
	tweet, create=Tweet.objects.get_or_create(username=status.username,\
                                                  text=text,datetime=status.datetime,\
                                                  source=status.source,inreply=inreply)
	if create:
            print "added"	
            #todo: Procesar(tweet)

        if status.reposted_by:
	    users = ''
	    for u in status.reposted_by:
	        users += u + ' '
	    print 'Retweeted by %s' % status.reposted_by
        print
        count += 1

turpial = Core()
for controller in Controller.objects.all():
    turpial.register_account(controller.user,controller.password,turpial.list_protocols()[int(controller.service)])

for acc in turpial.list_accounts():
    rtn = turpial.login(acc)
    if rtn.code > 0:
        print rtn.errmsg
    else:
        print 'Logged in with account %s' % acc.split('-')[0]

print "Ciclo de extraccion *****************"
while True:
    for acc in turpial.list_accounts():
        #Recibe tweets de cada cuenta
        rtn = turpial.get_column_statuses(acc, ColumnType.REPLIES)
        #Procesa los tweets
        process_statuses(rtn)



