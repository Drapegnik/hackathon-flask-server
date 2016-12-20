from flask import Flask
from flask_cors import CORS

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index, DocType, analyzer, Mapping
from elasticsearch_dsl import Search, Text, Long, Float

from collections import defaultdict

import json
import os

app = Flask(__name__)
CORS(app)

client = Elasticsearch(hosts='localhost')
index_name = "hackaton_frames"
s = Search(using = client, index = index_name)

@app.route('/search/')
def lol():
	return json.dumps([])
	
@app.route('/search/<search_text>')
def search_request(search_text):
	response = []
	videos_dict = defaultdict(list)
	
	results = s.query("match", text = search_text).execute()
	
	for res in results:
		vid_path = res.path_csv[:res.path_csv.index('-')]
		frame_path = (res.path_csv[:res.path_csv.index('-info')]).replace('\\','/')
		frame = {'frame_path' : frame_path, 'frame_sec' : res.frame_num, 
				'text' : res.text, 'frame_score' : res.meta.score}
		videos_dict[vid_path].append(frame)

	for video_path in videos_dict.keys():
		vid_score = 0
		if (len(videos_dict[video_path]) != 0):
			vid_score = float(sum(d['frame_score'] for d in videos_dict[video_path]))/len(videos_dict[video_path])
		response.append({'vid_path' : video_path, 'vid_score': vid_score, 'frames' : videos_dict[video_path]
						 })
	response_sorted = sorted(response, key=lambda k: k['vid_score'], reverse=True)

	return json.dumps(response_sorted)

@app.route('/')
def hello_world():
	return 'Hello!'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
