from crawlerino.models import tablerino
from crawlerino import db 
from bs4 import BeautifulSoup
import validators
import requests
import operator
import json

def api_get_url_from_db(get_id):
    get_id_query = tablerino.query.filter_by(json_id=get_id).first()
    result_id_from_get_id = get_id_query.json_id
    result_url_from_get_id = get_id_query.json_urlerino
    result_content_from_get_id = get_id_query.json_objecterino
    return result_id_from_get_id, result_url_from_get_id, result_content_from_get_id
    
def api_yeet(delete_id):
    tablerino.query.filter_by(json_id=delete_id).delete()
    db.session.commit()
    return 1

def scraperino(post_url):
    substringerino = 'wikipedia.org'
    if validators.url(post_url):
        if substringerino in post_url:
            get_json_tree(post_url)
        else:
            return {"message":"C'est quoi cette URL de con?"}

def page_reading(post_url):
    response = requests.get(post_url)
    soup = BeautifulSoup(response.content, features='lxml')
    link = soup.find('div', {'class': 'mw-parser-output'}).find_all('p')
    return link

def word_counting(text):
    counts = dict()
    words = text.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts

def word_count_merging(dict1, dict2):
    merged = dict1.copy()
    for key,value in dict2.items():
        if key in merged.keys():
            merged[key] += value
        else:
            merged[key] = value
    return merged

def full_page_word_counts(post_url):
    page = page_reading(post_url)
    final_count = dict()
    for t in page:
        word_count = word_counting(t.text)
        final_count = word_count_merging(final_count,word_count)
    return final_count

def get_json_tree(post_url):
    result = full_page_word_counts(post_url)
    sorted_r = dict(sorted(result.items(), key=operator.itemgetter(1),reverse=True))
    json_result = json.dumps(sorted_r, ensure_ascii=False)
    json_to_database(json_result, post_url)

def json_to_database(json_result, post_url):
    if db.session.query(tablerino.json_id).filter_by(json_urlerino=post_url).first() is None:
        new_json = tablerino(
            json_objecterino = json_result,
            json_urlerino = post_url
        )
        db.session.add(new_json)
        db.session.commit()
        return 1