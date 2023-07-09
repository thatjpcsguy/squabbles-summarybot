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
        return response.text
    
    return None


if __name__ == '__main__':
    url = 'https://apnews.com/article/south-korea-japan-fukushima-wastewater-iaea-37b42b2d442d15115dae462b48494fd6'

    article = parse_articlev2(url)
    if article:
        print(summarise(article))
