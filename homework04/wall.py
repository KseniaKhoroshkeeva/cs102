import pandas as pd
import requests
import textwrap

from gensim import corpora, models
from gensim.utils import simple_preprocess
#from pandas.io.json import json_normalize
#from string import Template
#from tqdm import tqdm
from time import sleep
from stopwords import stop_words

import config

allowed_alphabet = '-'
allowed_alphabet += 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
allowed_alphabet += 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=100,
    filt: str='owner',
    extended: int=0,
    fields: str='',
    v: str='5.103',
    n_queries: int=25) -> pd.DataFrame:

    code = 'return ['
    for i in range(n_queries):
        query = {
            'owner_id': owner_id,
            'domain': domain,
            'offset': offset + i * count,
            'count': count,
            'filt': filt,
            'extended': extended,
            'fields': fields,
            'v': v
        }
        code += f'API.wall.get({str(query)})'
        if i < n_queries - 1:
            code += ', '
        else:
            code += '];'
    
    response = requests.post(
    url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG['access_token'],
            "v": v
        }
    )
    return response


def get_model(
    domain: str='',
    num_topics: int=5,
    num_words: int=8,
    passes: int=5,
    max_requests: int=4):
    offset = 0
    texts = []
    end = False
    n = 0
    while True:
        queries = get_wall(domain=domain, offset=offset).json()['response']
        for q in queries:         
            posts = q['items']
            if len(posts):
                for p in posts:
                    texts.append(p['text'])
                    n += 1
            else:
                end = True
                break
        if end:
            break
        offset += 2500
        # print(offset)
        sleep(0.35)
        if offset >= max_requests * 2500:
            break
    print(f'Parsed {n} posts')
    normalized_texts = []
    for t in texts:
        t = t.lower().replace('\n', ' ')
        for ch in '.,!?:;':
            t = t.replace(ch, ' ')
        normalized_words = []
        for word in t.split():
            if 2 <= len(word) <= 20:
                ok_word = True
                for ch in word:
                    if ch not in allowed_alphabet:
                        ok_word = False
                        break
                if word in stop_words or ('-' in word and word.split('-')[0] in stop_words):
                    ok_word = False
                if ok_word:
                    normalized_words.append(word)
        normalized_texts.append(normalized_words)
    
    dictionary = corpora.Dictionary(normalized_texts)
    corpus = [dictionary.doc2bow(text, allow_update=True) for text in normalized_texts]
    model = models.LdaModel(
        corpus,
        id2word=dictionary,
        alpha='auto',
        num_topics=num_topics,
        passes=passes)
    for topic_id in range(model.num_topics):
        topic = model.show_topic(topic_id, num_words)
        topic_words = [w for w, _ in topic]
        print('Topic {}: {}'.format(topic_id + 1, ' '.join(topic_words)))