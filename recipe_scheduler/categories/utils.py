import urllib.request
from bs4 import BeautifulSoup


def parse_html(url):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

    req = urllib.request.Request(url, headers=headers)
    try:
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        descriptions = soup.find('meta',
                                 attrs={'name': 'og:description'})\
                       or soup.find('meta',
                                    attrs={'property': 'description'}) \
                       or soup.find('meta', attrs={'name': 'description'})
        title = soup.find('title')
        if descriptions:
            description = descriptions.get('content')
        #
        # if not description or not title:
        #     print("check error", r.id, r.recipe_url)

        return {'title': title.text, 'description': description}
    except urllib.error.URLError as e:
        return
