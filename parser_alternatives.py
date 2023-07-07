import requests
import html2text
from bs4 import BeautifulSoup

from transformers import AutoTokenizer, AutoModelWithLMHead


# from readability import Document
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}


def parse_articlev3(url):
    response = requests.get(url, headers=headers)
    doc = Document(response.content)
    summary = doc.summary()

    h = html2text.HTML2Text()

    # Ignore converting links and images from the article
    h.ignore_links = True
    h.ignore_images = True

    output = h.handle(doc.summary())

    return output



def parse_article(url):
    web_raw = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_raw.content, features="lxml")

    article = soup.article
    if article:

        doc = Document(str(article))

        h = html2text.HTML2Text()

        # Ignore converting links and images from the article
        h.ignore_links = True
        h.ignore_images = True

        output = h.handle(doc.summary())
        return output

    return None


def summarisev2(article):
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

    inputs = tokenizer.encode("summarize: " + article,
        return_tensors='pt',
        # model_max_length=512,
        truncation=True)
    
    summary_ids = model.generate(inputs, max_length=256, min_length=80, length_penalty=5., num_beams=2)
    summary = tokenizer.decode(summary_ids[0])

    return summary


if __name__ == '__main__':
    # article = parse_articlev3('https://www.cbc.ca/news/canada/toronto/stabbing-ttc-eglinton-1.6898949')
    article = parse_articlev3('https://mashable.com/article/twitter-elon-musk-threaten-lawsuit-meta-threads')
    summary = summarisev2(article)

    print(summary)
