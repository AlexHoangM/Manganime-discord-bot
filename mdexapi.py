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
        mangaID = titleData['results'][0]['data']['id']
    except:
        mangaID = None

    return mangaID


def mangaTitle(titleData):
    try:
        mangaTitle = titleData['results'][0]['data']['attributes']['title']['en']
    except KeyError:
        mangaTitle = titleData['results'][0]['data']['attributes']['title']['jp']
    except:
        mangaTitle = None

    return mangaTitle


def mangaDescription(titleData):
    try:
        mangaDescription = titleData['results'][0]['data']['attributes']['description']['en']
    except:
        mangaDescription = 'Not found'
    if '\r\n' in mangaDescription:
        mangaDescription = mangaDescription.split('\r\n')[0].strip()
    elif '\n' in mangaDescription:
        mangaDescription = mangaDescription.split('\n')[0].strip()
    return mangaDescription    
    

def mangaLink(titleData):
    try:
        ID = titleData['results'][0]['data']['id']
        mangaLink = f'https://mangadex.org/title/{ID}'
    except:
        mangaLink = 'Not found'

    return mangaLink

def mangaList(titleData):
    mangaList = []
    for i in range(10):
        try:
            mangaTitle = titleData['results'][i]['data']['attributes']['title']['en']
        except KeyError:
            mangaTitle = titleData['results'][i]['data']['attributes']['title']['jp']
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
        coverID = coverData['results'][0]['data']['attributes']['fileName']
    except:
        coverID = None

    return coverID

def chapterLink(mangaID, chapter):
    chapterLink = requests.get(f'https://api.mangadex.org/chapter?manga={mangaID}&&chapter={chapter}')
    chapterData = chapterLink.json()
    try:
        for i in range(len(chapterData)):
            if chapterData['results'][i]['data']['attributes']['translatedLanguage'] == 'en':
                chapID = chapterData['results'][i]['data']['id']
                chapLink = f'https://mangadex.org/chapter/{chapID}/1'
                break
            else:
                pass
    except:
        chapID = None
        chapLink = None
    return chapLink