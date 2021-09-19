import feedparser
from datetime import datetime
import logging


logger = logging.getLogger('__name__')

#Remove Tritinia Scans rss due to rss feed not updated
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
                
            #Format:    - Volume ... Chapter ...
            uncleanTitle = title.rsplit('- Volume')
            try:
                chapter = uncleanTitle[1].rsplit('Chapter')[1].strip()
            except IndexError:
                pass
            
            #Format:   - Vol. ... Ch. ...
            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('- Vol.')
                try:
                    chapter = uncleanTitle[1].rsplit('Ch.')[1].strip()
                except IndexError:
                    pass
            else:
                pass
            
            #Format:   - Vol. ... Chapter ...
            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('Vol.')
                try:
                    chapter = uncleanTitle[1].rsplit('Chapter')[1].strip()
                except IndexError:
                    pass
            else:
                pass
            
            #Format:   - Chapter ...
            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('- Chapter')
                try:
                    chapter = uncleanTitle[1].strip()
                except IndexError:
                    pass
            else:
                pass

            #Format:   - Ch. ...
            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('- Ch.')
                try:
                    chapter = uncleanTitle[1].strip()
                except IndexError:
                    pass
            else:
                pass
            
            #Format:   Chapter ... or Chapter ...: chaptitle
            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit('Chapter')
                try:
                    uncleanchapter = uncleanTitle[1].strip()
                    try:
                        chapter = uncleanchapter.rsplit(':')[0].strip()
                    except:
                        pass
                except IndexError:
                    pass
            else:
                pass

            #Format:  title ....
            if uncleanTitle[0] is title:
                uncleanTitle = title.rsplit(' ', 1)
                try:
                    chapter = uncleanTitle[1].strip()
                except IndexError:
                    pass
            else:
                pass

            #Format:    ... -  - Fabrication ...
            if 'Fabrication' in chapter:
                chapter = chapter.rsplit(' -  - Fabrication')[0].strip()
            #Format:    ... -  - Last Chapter - END
            elif 'Last Chapter' in chapter:
                chapter = chapter.rsplit(' -  - Last Chapter')[0].strip()
            #Format:   ...-...
            elif '-' in chapter:
                chapter = chapter.split('-', 1)[1].strip()
            elif '–' in chapter:
                chapter = chapter.split('–', 1)[0].strip()
            elif '&amp;' in chapter:
                chapter = chapter.split('&amp;', 1)
            else:
                pass

            cleanTitle = uncleanTitle[0].replace('–', '').replace('\\', '').replace('&#039;', '\'').strip()

            chaplist = []

            if type(chapter) == str:
                chaplist.append(chapter)
            elif type(chapter) == list:
                for i in chapter:
                    chaplist.append(i)

            unclchapter = list(filter(None, map(chaptoInt, chaplist)))
            #Note: ['0'] returns [] for Hatigarm scans and Lynx scans

            if len(unclchapter) == 1:
                cleanChapter = unclchapter[0]
            elif len(unclchapter) > 1:
                cleanChapter = unclchapter[1]
            else:
                cleanChapter = 0

            mangaInfo.append({'Title': cleanTitle, 'Chapter': cleanChapter, 'Date': pubdate, 'Author': author, 'Link': url})

    return mangaInfo