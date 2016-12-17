from flask import Flask
from flask_cors import CORS

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, DocType, analyzer, Mapping
from elasticsearch_dsl import Search, Text, Long, Float

import json

app = Flask(__name__)
CORS(app)

client = Elasticsearch(hosts='100.95.255.141')
index_name = "hackaton_frames"

@app.route('/search/<search_text>')
def search_request(search_text):
	print(search_text)
	response = []
	s = Search(using = client, index = index_name)
	for res in s.query("match", text = search_text):
		vid_path = res.path_csv[:res.path_csv.index('-')]
		frame_path = (res.path_csv[:res.path_csv.index('-info')]).replace('\\','/')
		response.append({'vid_path': vid_path, 'frame_path': frame_path, 'frame_sec': res.frame_num, 'score': res.meta.score,\
						 'theme': res.theme, 'text': res.text})

	return json.dumps(response)

@app.route('/')
def hello_world():
	return 'Hello!'


if __name__ == '__main__':
    app.run()
