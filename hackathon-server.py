from flask import Flask
from flask_cors import CORS

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, DocType, analyzer, Mapping
from elasticsearch_dsl import Search, Text, Long, Float

from collections import defaultdict

import json

app = Flask(__name__)
CORS(app)

client = Elasticsearch(hosts='100.95.255.141')
index_name = "hackaton_frames"

@app.route('/search/<search_text>')
def search_request(search_text):
	response = []
	s = Search(using = client, index = index_name)
	videos_dict = defaultdict(list)
	for res in s.query("match", text = search_text):
		vid_path = res.path_csv[:res.path_csv.index('-')]
		frame_path = (res.path_csv[:res.path_csv.index('-info')]).replace('\\','/')
		frame = {'frame_path' : frame_path, 'frame_sec' : res.frame_num, 
				'text' : res.text}
		videos_dict[vid_path].append(frame)

	for video_path in videos_dict.keys():
		response.append({'vid_path' : video_path, 'frames' : videos_dict[video_path]})

	return json.dumps(response)

@app.route('/')
def hello_world():
	return 'Hello!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
