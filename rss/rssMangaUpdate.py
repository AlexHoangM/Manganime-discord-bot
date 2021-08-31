import feedparser
import logging


logger = logging.getLogger('__name__')


def rssParser():

    rss = 'https://www.mangaupdates.com/rss.php'
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

        date = entry['summary']
        date = date.split('<br')[0]

        group = title[title.index('[')+1: title.index(']')]

        uncleanTitle = title.split(f'[{group}]')[1]

        unclTitle = uncleanTitle.rsplit('v.')
        try:
            chapter = unclTitle[1].rsplit('c.')[1].strip()
        except IndexError:
            pass

        if unclTitle[0] is uncleanTitle:
            unclTitle = uncleanTitle.rsplit('c.')
            try:
                chapter = unclTitle[1].strip()
            except IndexError:
                pass
        else:
            pass

        if '-' in chapter:
            chapter = chapter.split('-', 1)
            chapter = chapter[1]
        else:
            pass

        cleanTitle = unclTitle[0].strip()
    
        mangaInfo.append({'Title': cleanTitle, 'Chapter': chapter, 'Date': date, 'Author': group, 'Link': '', 'Source': 'MangaUpdate'})
    
    return mangaInfo