import requests
 

def titleResult(title):
    title = title.replace(' ', '+')
    titleResponse = requests.get(f'https://api.mangadex.org/manga?title={title}')
    titleData = titleResponse.json()
    if titleData['data'] == []:
        titleData = None
    else:
        pass
    return titleData


def mangaID(titleData):
    try:
        mangaID = titleData['data'][0]['id']
    except:
        mangaID = None

    return mangaID


def mangaTitle(titleData):
    try:
        mangaTitle = titleData['data'][0]['attributes']['title']['en']
    #except KeyError:
    #    mangaTitle = titleData['results'][0]['attributes']['title']['jp']
    except:
        mangaTitle = None

    return mangaTitle


def mangaDescription(titleData):
    try:
        mangaDescription = titleData['data'][0]['attributes']['description']['en']
    except:
        mangaDescription = 'Not found'
    if '\r\n' in mangaDescription:
        mangaDescription = mangaDescription.split('\r\n')[0].strip()
    elif '\n' in mangaDescription:
        mangaDescription = mangaDescription.split('\n')[0].strip()
    return mangaDescription    
    

def mangaLink(titleData):
    try:
        ID = titleData['data'][0]['id']
        titleLink = mangaTitle(titleData).lower().replace(',','').replace(' ','-')
        mangaLink = f'https://mangadex.org/title/{ID}/{titleLink}'
    except:
        mangaLink = 'Not found'

    return mangaLink

def mangaList(titleData):
    mangaList = []
    for i in range(10):
        try:
            mangaTitle = titleData['data'][i]['attributes']['title']['en']
        #except KeyError:
        #    mangaTitle = titleData['results'][i]['data']['attributes']['title']['jp']
        except IndexError:
            pass

        mangaList.append(mangaTitle)
        
    resList = [i for n, i in enumerate(mangaList) if i not in mangaList[:n]]

    return resList


def coverResult(mangaID):
    coverResponse = requests.get(f'https://api.mangadex.org/cover?manga[]={mangaID}')
    coverData = coverResponse.json() 
    
    return coverData


def coverID(coverData):
    try:
        coverID = coverData['data'][0]['attributes']['fileName']
    except:
        coverID = None

    return coverID

def chapterLink(mangaID, chapter):
    chapterLink = requests.get(f'https://api.mangadex.org/chapter?manga={mangaID}&&chapter={chapter}')
    chapterData = chapterLink.json()
    try:
        for i in range(len(chapterData)):
            if chapterData['data'][i]['attributes']['translatedLanguage'] == 'en':
                chapID = chapterData['data'][i]['id']
                chapLink = f'https://mangadex.org/chapter/{chapID}/1'
                break
            else:
                pass
    except:
        chapID = None
        chapLink = None
    return chapLink