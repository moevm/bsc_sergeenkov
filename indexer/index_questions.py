import requests
import re
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

ENCODER_URL = 'http://100.124.0.10:5000/encode-sentences'
ELASTICSEARCH_URL = 'http://100.124.0.10:9200'
INDEX_NAME = 'qa_index'
INDEX_FILE = 'index.json'
COMMENTS_FILE = '../data/comments.json'

questions = [
    'Что такое MAC-адрес?',
    'Зачем нужен MAC-адрес?',
    'Как расчитать маску подсети?',
    'Как связаны маска подсети и физический адрес?'
]

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub(' ', text).strip()


def prepare_questions():
    comments = None
    with open(COMMENTS_FILE, 'r') as file_obj:
        comments = json.loads(file_obj.read())
    if comments is None:
        raise Exception('No comments to index')
    prepared_questions = []
    for comment in comments:
        text = remove_tags(comment['text'])
        prepared_questions.append(text)
    return prepared_questions


def get_sentence_vector(sentence):
    response = requests.post(
        url=ENCODER_URL,
        json={'sentences': [sentence]}
    )
    if response.status_code != 200:
        raise Exception('Encoder error')
    return response.json()['vectors'][0]


def handle_query(query):
    client = Elasticsearch(ELASTICSEARCH_URL)
    query_vector = get_sentence_vector(query)
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['title_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body={
            "size": 5,
            "query": script_query,
            "_source": {"includes": ["title"]}
        }
    )
    print()
    print("{} total hits.".format(response["hits"]["total"]["value"]))
    for hit in response["hits"]["hits"]:
        print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
        print(hit["_source"])
        print()


if __name__ == '__main__':
    client = Elasticsearch(ELASTICSEARCH_URL)
    client.indices.delete(index=INDEX_NAME, ignore=[404])
    with open(INDEX_FILE) as index_file:
        source = index_file.read().strip()
        client.indices.create(index=INDEX_NAME, body=source)

    comments = prepare_questions()

    response = requests.post(
        url=ENCODER_URL,
        json={'sentences': comments}
    )

    if response.status_code != 200:
        raise Exception('Encoder error')

    title_vectors = response.json()['vectors']

    elastic_requests = []

    for i, question in enumerate(comments):
        elastic_requests.append({
            'title': question,
            'title_vector': title_vectors[i],
            '_op_type': 'index',
            '_index': INDEX_NAME
        })
    bulk(client, elastic_requests)
    client.indices.refresh(index=INDEX_NAME)
