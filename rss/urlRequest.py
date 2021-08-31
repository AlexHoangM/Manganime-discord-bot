import urllib.request as urlrequest
from bs4 import BeautifulSoup

#Fixed Constant
HEADER = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8',
'Connection': 'keep-alive'}

def urlRequester(url):

    request = urlrequest.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    response = urlrequest.urlopen(request).read()

    html = response.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    return soup