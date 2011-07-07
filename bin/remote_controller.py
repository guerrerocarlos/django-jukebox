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
from apps.music_player.models import SongRequest 
from apps.music_db.models import Song
from libturpial.api.core import Core
from libturpial.common import clean_bytecodes, ColumnType

class Remote():
    def __init__(self):
        self.turpial = Core()
        for controller in Controller.objects.all():
            self.turpial.register_account(controller.user,controller.password,self.turpial.list_protocols()[int(controller.service)])

        for acc in self.turpial.list_accounts():
            rtn = self.turpial.login(acc)
            if rtn.code > 0:
                print rtn.errmsg
            else:
                print 'Logged in with account %s' % acc.split('-')[0]

        print "Ciclo de extraccion *****************"
        while True:
            for acc in self.turpial.list_accounts():
#                rtn = self.turpial.get_column_statuses(acc, ColumnType.DIRECTS)
#                self.process_statuses(rtn)
                rtn = self.turpial.get_column_statuses(acc, ColumnType.REPLIES)
                self.process_statuses(rtn)


    
    def procesar(self,tweet):
        if tweet.text.find("#") > -1:
            pos=tweet.text[tweet.text.find("#"):].find(" ")
            if pos == -1:
                pos = len(tweet.text[tweet.text.find("#"):])
            print "pos: "+str(pos)

            print "buscando :"+tweet.text[tweet.text.find("#"):tweet.text.find("#")+pos]
            song = Song.objects.get(id=int(tweet.text[tweet.text.find("#")+1:int(tweet.text.find("#")+pos)]))
            if SongRequest.objects.get_active_requests().filter(song=song):
                # Don't allow requesting a song that is currently in the queue.
                print "Song has already been requested."
            else:
                # Song isn't already in the SongRequest queue, add it.
                request = SongRequest(song=song, twitter=tweet.username)
                request.save()
                rtn = self.turpial.update_status(self.turpial.list_accounts()[0], "@"+tweet.username+" puso en cola de reproduccion a: "+song.title+" - "+song.artist)
                if rtn.code > 0:
                    print rtn.errmsg
                else:
                    print '\n\n\n\nMessage posted in account %s' % self.turpial.list_accounts()[0].split('-')[0]
                print "***************Song Requested.\n\n\n\n\n"


    def process_statuses(self,statuses):
        if statuses.code > 0:
            print statuses.errmsg
            return

        count = 1

        for status in statuses[::-1]:
            text = status.text.replace('\n', ' ')
            inreply = ''
            if status.in_reply_to_user:
                inreply = ' en respuesta a %s' % status.in_reply_to_user
            tweet, create =Tweet.objects.get_or_create(username=status.username,\
                                                      text=text,datetime=status.datetime,\
                                                      source=status.source,inreply=inreply)
            if create :
                print "added"	
                self.procesar(tweet)

            if status.reposted_by:
                users = ''
                for u in status.reposted_by:
                    users += u + ' '
                print 'Retweeted by %s' % status.reposted_by
                print
            count += 1


if __name__ == "__main__":
    remote = Remote()
