import feedparser
from datetime import datetime
import logging


logger = logging.getLogger('__name__')


rssScanlator = {'Arang Scans': 'https://arangscans.com/rss',
'Flame Scans'         : 'https://flamescans.org/feed/',
'Hatigarm Scans'      : 'https://hatigarmscanz.net/feed',
'Hunlight Scans'      : 'https://hunlight-scans.info/feed',
'Kirei Cake'          : 'https://kireicake.com/feed/',
'LHTranslation'       : 'https://lhtranslation.net/manga-rss.rss',
'Lynx Scans'          : 'https://lynxscans.com/feed',
'Mangasushi'          : 'https://mangasushi.net/feed/manga-chapters',
'MethodScan'          : 'https://methodscans.com/feed',
'NANI? Scans'         : 'https://naniscans.com/rss',
'SensesScans'         : 'https://sensescans.com/index.php?action=.xml;type=rss;board=45.0;sa=news',
'Tritinia Scans'      : 'https://rss.tritinia.com/all-series.xml',
'WhimSubs'            : 'https://whimsubs.xyz/r/feeds/rss.xml',
'Zero Scans (Discord)': 'https://zeroscans.com/feed'}


def chaptoInt(string):
    if not string:
        return string

    try:
        floatn = float(string)
        inte = int(floatn)

        return inte if floatn == inte else floatn
    except ValueError:
        pass


def rssParser():
    
    mangaInfo = []
    
    for author in rssScanlator:

        try:
            data = feedparser.parse(rssScanlator[author])
        except:
            data = None

            while data == None:
                try:
                    data = feedparser.parser(rssScanlator[author])               
                except:
                    continue


        entries = data.entries
        dateFormat = ['%a, %d %b %Y %H:%M:%S %Z', '%a, %d %b %Y %H:%M:%S Z', '%a, %d %b %Y %H:%M:%S +0000', '%a, %d %b %Y %H:%M:%S +0400']


        for entry in entries:

            title = entry['title']
            url = entry['link']                
            
            try:
                date = entry['published']
            except KeyError:
                date = entry['updated']

            try:
                for i in range(len(dateFormat)):
                    
                    try:
                        pubdate = datetime.strptime(date, dateFormat[i]).strftime('%Y-%m-%d')
                    except ValueError:
                        continue
            except KeyError:
                pubdate = datetime.today().strftime('%Y-%m-%d')
                
            uncleanTitle = title.rsplit('- Volume')
            try:
                chapter = uncleanTitle[1].rsplit('Chapter')[1].strip()
            except IndexError:
                pass

            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('- Vol.')
                try:
                    chapter = uncleanTitle[1].rsplit('Ch.')[1].strip()
                except IndexError:
                    pass
            else:
                pass

            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('Vol.')
                try:
                    chapter = uncleanTitle[1].rsplit('Chapter')[1].strip()
                except IndexError:
                    pass
            else:
                pass

            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('- Chapter')
                try:
                    chapter = uncleanTitle[1].strip()
                except IndexError:
                    pass
            else:
                pass

            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('- Ch.')
                try:
                    chapter = uncleanTitle[1].strip()
                except IndexError:
                    pass
            else:
                pass

            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('Chapter')
                try:
                    chapter = uncleanTitle[1].strip()
                except IndexError:
                    pass
            else:
                pass

            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit(' ', 1)
                try:
                    chapter = uncleanTitle[1].strip()
                except IndexError:
                    pass
            else:
                pass

            if '-' in chapter:
                chapter = chapter.split('-', 1)
            elif '&amp;' in chapter:
                chapter = chapter.split('&amp;', 1)
            else:
                pass

            cleanTitle = uncleanTitle[0].replace('–', '').replace('\\', '').strip()

            chaplist = []

            if type(chapter) == str:
                chaplist.append(chapter)
            elif type(chapter) == list:
                for i in chapter:
                    chaplist.append(i)

            unclchapter = list(filter(None, map(chaptoInt, chaplist)))

            if len(unclchapter) == 1:
                cleanChapter = unclchapter[0]
            elif len(unclchapter) > 1:
                cleanChapter = unclchapter[1]
            else:
                cleanChapter = ''

            mangaInfo.append({'Title': cleanTitle, 'Chapter': cleanChapter, 'Date': pubdate, 'Author': author, 'Link': url, 'Source': author})

    return mangaInfo

print(rssParser())