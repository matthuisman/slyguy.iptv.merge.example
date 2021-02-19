import sys
import codecs
from xml.sax.saxutils import escape

import xbmcplugin, xbmcgui, xbmcaddon

try:
    #Python3
    from urllib.parse import parse_qsl, quote
except:
    #Python2
    from urlparse import parse_qsl
    from urllib import quote

ADDON = xbmcaddon.Addon()

params = dict(parse_qsl(sys.argv[2].lstrip('?'), keep_blank_values=True))
method = params.get('method')
handle = int(sys.argv[1])

example_url = 'https://bitmovin-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8'
channels = {
    'ch1': {'chno': 1, 'name': 'Channel 1', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/1/10/Paraguay_TV_logo.png', 'url': example_url},
    'ch2': {'chno': 2, 'name': 'Channel 2', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/1/10/Paraguay_TV_logo.png', 'url': example_url},
    'ch3': {'chno': 3, 'name': 'Channel 3', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/1/10/Paraguay_TV_logo.png', 'url': example_url},
    'ch4': {'chno': 4, 'name': 'Channel 4', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/1/10/Paraguay_TV_logo.png', 'url': example_url},
    'ch5': {'chno': 5, 'name': 'Channel 5', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/1/10/Paraguay_TV_logo.png', 'url': example_url},
}

epg = {'start': '20210217103000 +0000', 'stop': '20250220103000 +0000', 'title': 'Example EPG', 'desc': 'Example EPG description'}

def write_playlist(filepath):
    with codecs.open(filepath, 'w', encoding='utf8') as f:
        f.write(u'#EXTM3U\n')

        for channel_id in channels:
            channel = channels[channel_id]
            play_path = 'plugin://{}/?method=play&channel_id={}'.format(ADDON.getAddonInfo('id'), channel_id)
            f.write(u'#EXTINF:-1 tvg-id="{id}" tvg-chno="{chno}" tvg-logo="{logo}",{name}\n{path}\n'.format(
                        id=channel_id, chno=channel['chno'], logo=channel['logo'], name=channel['name'], path=play_path))

def write_epg(filepath):
    with codecs.open(filepath, 'w', encoding='utf8') as f:
        f.write(u'<?xml version="1.0" encoding="utf-8" ?><tv>')

        for i in range(10000):
            f.write(u'<blah id="123"></blah>')

        for channel_id in channels:
            channel = channels[channel_id]

            f.write(u'<channel id="{}"><display-name>{}</display-name><icon src="{}"/></channel>'.format(
                channel_id, escape(channel['name']), escape(channel['logo'])))

            f.write(u'<programme channel="{}" start="{}" stop="{}"><title>{}</title><desc>{}</desc></programme>'.format(
                channel_id, epg['start'], epg['stop'], escape(epg['title']), escape(epg['desc'])))

        f.write(u'</tv>')

if method in ('epg', 'playlist'):
    try:
        if method == 'epg':
            write_epg(params.get('output'))
        elif method == 'playlist':
            write_playlist(params.get('output'))
    except Exception as e:
        message = str(e)
    else:
        message = 'ok'

    xbmcplugin.addDirectoryItem(handle, quote(message), xbmcgui.ListItem())
    xbmcplugin.endOfDirectory(handle, succeeded=True)

elif method == 'play':
    channel_id = params.get('channel_id')
    channel = channels[channel_id]

    li = xbmcgui.ListItem(channel['name'])
    li.setPath(channel['url'])
    xbmcplugin.setResolvedUrl(handle, True, li)

else:
    setup_path = 'plugin://plugin.program.iptv.merge/?_=setup_addon&addon_id=' + ADDON.getAddonInfo('id')
    li = xbmcgui.ListItem('Add Me to IPTV Merge')
    li.setPath(setup_path)
    xbmcplugin.addDirectoryItem(handle, setup_path, li, False)
    xbmcplugin.endOfDirectory(handle, succeeded=True)