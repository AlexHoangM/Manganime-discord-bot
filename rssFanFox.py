import feedparser
from datetime import datetime
import logging


logger = logging.getLogger('__name__')


def rssParser():

    rss = 'https://feeds2.feedburner.com/mangafox/latest_manga_chapters'
    
    mangaInfo = []    

    try:
        data = feedparser.parse(rss)

    except:
        data = None

        while data == None:
            try:
                data = feedparser.parser(rss)
            except:
                return None

    entries = data.entries

    for entry in entries:
        title = entry['title']
        
        date = entry['published']
        date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')
        
        url = entry['feedburner_origlink']

        uncleanTitle = title.rsplit('Vol.')
        try:
            chapter = uncleanTitle[1].rsplit('Ch.')[1].strip()
        except IndexError:
            pass

        if uncleanTitle[0] is title:
            uncleanTitle = title.rsplit('Ch.')
            try:
                chapter = uncleanTitle[1].strip()
            except IndexError:
                pass

        cleanTitle = uncleanTitle[0].replace('&apos;', '\'').replace('%26', '&').strip()

        mangaInfo.append({'title': cleanTitle, 'Chapter': chapter, 'Date': date, 'Author': '' , 'Link': url, 'Source': 'FanFox'})    
    
    return mangaInfo