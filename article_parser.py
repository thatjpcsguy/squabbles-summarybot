from newspaper import Article

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


LANGUAGE = "english"
SENTENCES_COUNT = 6

def parse_articlev2(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return None


def summarise(article):
    parser = PlaintextParser.from_string(article, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = [str(sentence) for sentence in summarizer(parser.document, SENTENCES_COUNT)]

    return '\n'.join(summary)
