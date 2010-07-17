#! /usr/bin/env python
# -*- coding: utf-8 -*-

#Copyright (C) 2008-2009 concentricpuddle

#This file is part of puddletag, a semi-good music tag editor.

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
import sys, pdb, os, time
from puddlestuff.puddleobjects import gettags, getfiles, PuddleConfig
from collections import defaultdict
from puddlestuff.constants import TAGSOURCE, HOMEDIR, TEXT, COMBO, CHECKBOX
from puddlestuff.util import matching, split_by_tag
from puddlestuff.tagsources import set_status, write_log
from puddlestuff.audioinfo import stringtags
#print 'example2'

properties = {'type': TAGSOURCE}

#musicdir = '/mnt/variable/Music'
#dirs = [unicode(z, 'utf8') for z in os.listdir(musicdir)]
try:
    image = [{'data': open(os.path.join(HOMEDIR, 'flux/image.jpg'), 'rb').read()}]
except:
    image = {}
    raise

def equal(audio1, audio2, play=False, tags=('artist', 'album')):
    for key in tags:
        if (key in audio1) and (key in audio2):
            if u''.join(audio1[key]).lower() != u''.join(audio2[key]).lower():
                return False
        else:
            return False
    if play and 'play' not in audio2:
        return False
    return True

class Example(object):
    name = 'Example'
    group_by = ['artist', 'album']
    counter = 0

    def __init__(self):
        object.__init__(self)
        cparser = PuddleConfig()
        musicdir = cparser.get('exampletagsource', 'musicdir', HOMEDIR)
        self.preferences = [['Music &Directory: ', TEXT, musicdir]]
        self.applyPrefs([musicdir])

    def search(self, artist, albums):
        ret = []
        matches = {}
        #set_status(u'Searching %s - %s' % (artist, albums[0]))
        ##write_log(u'Retrieving %s %s' % (artist, albums[0]))
        artist = artist.encode('utf8')
        albumtuple = [z.split(' - ', 1) for z in self._dirs 
            if z.startswith(artist) and ' - ' in z]
        albumtuple = [(i.decode('utf8'), z.decode('utf8')) for i, z  in albumtuple]
        releases = []
        for z in albumtuple:
            if len(z) > 1:
                releases.append(z[1])
        #if not releases:
            #set_status('No releases found')
            #write_log('No releases found for %s' % artist)
        #else:
            #write_log('Found albums <b>%s</b>' % u', '.join(releases))
        artist = artist.decode('utf8')
        matched = []
        low_releases = [z.lower() for z in releases]
        for album in albums:
            info = {'album': album, 'artist': artist}
            info['#extrainfo'] = ('Home Folder', u'file://' + HOMEDIR)
            if album.lower() in low_releases:
                if album.lower() in low_releases:
                    return [(info, [])]
        get_info = lambda album: {'artist': artist, 'album': album,
            u'#extrainfo': ('Home Folder', u'file:///' + HOMEDIR)}
        return [(get_info(album), []) for album in releases]

    def retrieve(self, info):
        if False:
            artist = 'Alicia Keys'
            album = 'As I Am'
        else:
            artist = info['artist']
            album = info['album']
            self.counter += 1
        dirpath = u'%s/%s - %s' % (self.musicdir, artist, album)
        files = []
        for f in gettags(getfiles(dirpath)):
            if f:
                #tag = stringtags(f.usertags)
                #tag['__image'] = image
                files.append(f.usertags)
        return info, files

    def applyPrefs(self, values):
        musicdir = values[0]
        self.musicdir = musicdir
        cparser = PuddleConfig()
        cparser.set('exampletagsource', 'musicdir', musicdir)
        self.preferences[0][2] = musicdir
        isdir = os.path.isdir
        join = os.path.join
        musicdir = musicdir.encode('utf8')
        self._dirs = [z for z in os.listdir(musicdir) if isdir(join(musicdir,z))]

info = [Example, None]
name = 'Example'

if __name__ == '__main__':
    x = Example()
    d = x.search('Angie Stone', ['The Very Best Of'])
    print x.retrieve(d[0][0])
    