from trafilatura import fetch_url, extract
import requests

LANGUAGE = "english"
SENTENCES_COUNT = 6

def parse_article(url):
    try:
        downloaded = fetch_url(url)
        if downloaded:
            result = extract(downloaded)
            return result
    except:
        return None


def summarise(article):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'content-type': 'text/plain;charset=UTF-8',
    }
    data = {
            "text": article[-14500:] if len(article) > 14500 else article,
            "locale": "en"
    }

    response = requests.post(
        'https://wordcount.com/api/summarize',
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.text.encode("latin-1").decode('utf-8')
    
    return None


if __name__ == '__main__':
    url = 'https://variety.com/2023/digital/news/colleen-ballinger-canceled-tour-dates-podcast-trisha-paytas-1235666512/'

    article = parse_article(url)

    if article:
        print(summarise(article))
