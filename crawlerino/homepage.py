from flask import render_template, flash, Blueprint, request
from crawlerino import db
from crawlerino.models import tablerino
import requests
import operator
import json
import validators
from bs4 import BeautifulSoup

homepage = Blueprint('homepage', __name__)

@homepage.route('/', methods=['GET', 'POST'])
def home_page():
    substringerino = 'wikipedia.org'
    formerino = request.form
    if request.method == 'POST':
        url_to_scrape = formerino.get('scrapyard')
        if formerino.get('scrapyard'):
            if validators.url(url_to_scrape):
                if substringerino in url_to_scrape:
                    get_json_tree(url_to_scrape)
                else:
                    flash("POURQUOI C'EST PAS UN LIEN WIKIPEDIA?! (ಠ益ಠ)", category='error')
            else:
                flash("C'EST QUOI CETTE URL DE MERDE?! (ಠ益ಠ)", category='error')
        elif formerino.get('shadow_realm'):
            yeet()
        else:
            flash("ELLE EST OÙ MON URL?! ٩(ఠ益ఠ)۶", category='error')
    url_list = get_url_from_db()
    max_url = len(url_list)
    return render_template('homepage.html', url_list_param=url_list, max_url_param=max_url)

def page_reading(url_to_scrape):
    response = requests.get(url_to_scrape)
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

def full_page_word_counts(url_to_scrape):
    page = page_reading(url_to_scrape)
    final_count = dict()
    for t in page:
        word_count = word_counting(t.text)
        final_count = word_count_merging(final_count,word_count)
    return final_count

def get_json_tree(url_to_scrape):
    result = full_page_word_counts(url_to_scrape)
    sorted_r = dict(sorted(result.items(), key=operator.itemgetter(1),reverse=True))
    json_result = json.dumps(sorted_r, ensure_ascii=False)
    json_to_database(json_result, url_to_scrape)

def json_to_database(json_result, url_to_scrape):
    url_list = get_url_from_db()
    max_url = len(url_list)
    if db.session.query(tablerino.json_id).filter_by(json_urlerino=url_to_scrape).first() is None:
        new_json = tablerino(
            json_objecterino = json_result,
            json_urlerino = url_to_scrape
        )
        db.session.add(new_json)
        db.session.commit()

        flash("C'EST DANS LA BASE! T'ES VRAIMENT TROP FORT! ᕕ( ᐛ )ᕗ", category='success')
    else:
        flash ("POURQUOI TU AJOUTES DEUX FOIS LA MÊME PAGE?! T'ES CON OU QUOI?! (‡▼益▼)", category='error')
    return render_template('homepage.html', url_list_param=url_list, max_url_param=max_url)

def get_url_from_db():
    url_query = tablerino.query.with_entities(tablerino.json_urlerino).distinct()
    url_list = []
    for url in url_query:
        url_list.append(url[0])
    return url_list

def yeet():
    db.session.query(tablerino).delete()
    db.session.commit()
