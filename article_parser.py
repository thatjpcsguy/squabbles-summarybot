from trafilatura import fetch_url, extract

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import requests

LANGUAGE = "english"
SENTENCES_COUNT = 6

def parse_articlev2(url):
    try:
        downloaded = fetch_url(url)
        if downloaded:
            result = extract(downloaded)
            return result
    except:
        return None


def summarise(article):
    parser = PlaintextParser.from_string(article, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)]

    if len(summary) > 2:
        summary[2] = summary[2] + '\n'

    return ' \n'.join(summary)


def summarise_online(article):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'content-type': 'text/plain;charset=UTF-8',
    }
    data = {
            "text": article,
            "locale": "en"
    }

    response = requests.post(
        'https://wordcount.com/api/summarize',
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        return response.text
    
    print(response.text)
    return summarise(article)




if __name__ == '__main__':
    url = 'https://www.dexerto.com/overwatch/overwatch-2-team-reveals-plans-to-bring-hanamura-back-as-a-dope-new-map-2204066/'


    article = parse_articlev2(url)
    if article:
        print(summarise_online(article))