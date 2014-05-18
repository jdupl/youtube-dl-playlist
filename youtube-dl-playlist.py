#!/usr/bin/python3
# youtube-dl-playlist
#
# Utility to download Youtube playlist videos.
# Forked to support python 3 and keep playlist's video order.
#
# @author Jordon Mears <jordoncm at gmail dot com>
# @author Justin Duplessis <duplessisjustin1 at gmail dot com>
# @license LGPL version 2 or greater <http://www.gnu.org/licenses/lgpl.html>

import sys
import urllib.request
import http.client
import json
import os
import glob


class PlaylistDownloader:
    target_dir = ''
    total_videos = 0
    downloaded = 0

    def set_target(self, target):
        self.target_dir = os.path.realpath(target) + '/'
        return self.target_dir

    def download(self, playlist_id):
        print('Getting playlist information ...')
        data = self.fetch_info(playlist_id)
        self.total_videos = int(data['feed']['openSearch$totalResults']['$t'])
        print('Total videos to download: {:d}'.format(self.total_videos))
        title = data['feed']['title']['$t']
        playlist_dir = self.create_path(self.target_dir, title)
        os.chdir(self.set_target(playlist_dir))

        self.downloaded = 1
        while(self.downloaded <= self.total_videos):
            data = self.fetch_info(playlist_id, self.downloaded, 50)
            self.download_entires(data['feed']['entry'])

    def download_entires(self, entries):
        for entry in entries:
            group = entry['media$group']
            if self.download_entry(group['yt$videoid']['$t'],
            group['media$title']['$t']):
                self.downloaded = self.downloaded + 1

    def download_entry(self, yt_id, yt_title):
        playlist_pos = str(self.downloaded).zfill(3)
        print("{:s}({:s}) {:s}".format(yt_id, playlist_pos, yt_title))

        existing = glob.glob('*' + yt_id + '.*')
        filtered = [x for x in existing if not x.endswith('part')]
        if filtered.__len__() > 0:
            print('alreary exists, skipping...')
            return True
        try:
            url = 'http://www.youtube.com/watch?v={:s}'.format(yt_id)
            file_name = '[{:s}]%(title)s[%(id)s].%(ext)s'.format(playlist_pos)
            proc = 'youtube-dl --audio-format=best -o "{:s}" {:s}'.format(
                file_name, url)
            os.system(proc)
            return True

        except KeyboardInterrupt:
            sys.exit(1)

        except Exception as e:
            print('failed: {:s}'.format(e.strerror))
            return False

    def fetch_info(self, playlist_id, start=1, limit=0):
        connection = http.client.HTTPConnection('gdata.youtube.com')
        connection.request('GET', '/feeds/api/playlists/' + str(playlist_id) +
        '/?' + urllib.parse.urlencode({
                'alt': 'json',
                'max-results': limit,
                'start-index': start,
                'v': 2
            }))

        response = connection.getresponse()
        if response.status != 200:
            print('Error: Not a valid/public playlist.')
            sys.exit(1)

        data = response.read()
        data = json.loads(data.decode('utf8'))
        return data

    def create_path(self, path, title):
        title = title.replace('/', '')
        number = ''

        if (os.path.exists(path + title) is True and
         os.path.isdir(path + title) is False):
            while(os.path.exists(path + title + str(number)) is True and
             os.path.isdir(path + title + str(number)) is False):
                if number == '':
                    number = 0
                number = number + 1

        if os.path.exists(path + title + str(number)) is False:
            os.mkdir(path + title + str(number))

        return path + title + str(number)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: youtube-dl-playlist PLAYLIST_ID [DESTINATION_PATH]')
        sys.exit(1)
    else:
        if sys.argv[1][0] == 'P' and sys.argv[1][1] == 'L':
            PLAYLIST_ID = sys.argv[1][2:]
        else:
            PLAYLIST_ID = sys.argv[1]
    downloader = PlaylistDownloader()
    if len(sys.argv) == 3:
        downloader.set_target(sys.argv[2] + '/')
    else:
        downloader.set_target('./')
    downloader.download(PLAYLIST_ID)
