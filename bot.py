
import requests

from article_parser import parse_article, summarise

from urllib.parse import urlparse
import pickle
import sys
import os

skip_communities = []
skip_authors = ['catullus48108']


def exists(h, path='cache'):
    if '--nocache' in sys.argv:
        return False
    if os.path.isfile(path + '/%s.pickle' % h):
        return True
    return False


def save(h, x, path='cache'):
    with open(path + '/%s.pickle' % h, 'wb') as f:
        pickle.dump(x, f)
        return x


def load(h, path='cache'):
    with open(path + '/%s.pickle' % h, 'rb') as f:
        return pickle.load(f)


def load_news_domains():
    domains = []
    with open('data/domains_whitelist.txt') as txt:
        for row in txt:
            domains.append(row.strip())

    return domains


def load_unknown_domains():
    domains = []
    with open('data/domains_unknown.txt') as txt:
        for row in txt:
            domains.append(row.strip())

    return domains


def load_blacklist():
    domains = []
    with open('data/domains_blacklist.txt') as txt:
        for row in txt:
            domains.append(row.strip())

    return domains


def unknown_domain(domain):
    with open('data/domains_unknown.txt', "a") as f:
        f.write(domain + "\n")


def post_reply(post_id, summary):

    if exists(post_id):
        return
    
    # TODO: Replace with login flow or something more legit
    if 'SQUABBLES_TOKEN' not in os.environ and not os.environ['SQUABBLES_TOKEN']:
        print("squabbles token broken / missing")
        exit()
    

    headers = {
        'authorization': 'Bearer ' + os.environ['SQUABBLES_TOKEN']
    }
    resp = requests.post(f'https://squabbles.io/api/posts/{post_id}/reply', data={
        "content": summary
    }, headers=headers)



    if resp.status_code != 201:
        print(post_id)
        print(resp)
        print(resp.json())
        exit()

    save(post_id, summary)


news_domains = load_news_domains()
domains_blacklist = load_blacklist()
unknown_domains = load_unknown_domains()

def get_latest_posts(page=1):
    feed = 'feed/all' # s/news/posts

    headers = {
        'authorization': 'Bearer ' + os.environ['SQUABBLES_TOKEN']
    }
    resp = requests.get(f'https://squabbles.io/api/{feed}?page={page}&sort=new&', headers=headers)
    data = resp.json()

    if 'data' not in data:
        print(data)
        exit()

    for post in data['data']:
        post_id = post['hash_id']

        if post['community_name'] in skip_communities:
            continue

        if post['author_username'] in skip_authors:
            continue

        if exists(post_id):
            continue

        if post['url_meta'] and post['url_meta']['type'] != 'image':
            o = urlparse(post['url_meta']['url'])

            domain = o.hostname
            if domain.startswith('www.'):
                domain = domain[4:]

            if domain in domains_blacklist or domain in unknown_domains:
                continue

            if o.hostname in news_domains or domain in news_domains:
                s = parse_article(post['url_meta']['url'])
                if s:
                    s = summarise(s)
                    if s:
                        post_reply(post_id, s)
                        print("Posted: " + post_id)
                    else:
                        print(s)
                        print(post)
                        print("Failed: " + post_id)
                else:
                    print(post)
                    print("Failed: " + post_id)
            else:
                print(domain + ' -> ' + post['url_meta']['url'])
                unknown_domain(domain)
                unknown_domains.append(domain)

    if data['current_page'] < 5 and data['next_page_url']:
        get_latest_posts(page=page+1)


if __name__ == '__main__':
    get_latest_posts()
