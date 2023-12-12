from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
import requests
import os
import json

json_file_path = "C:\\Users\\mengfany\\Documents\\umich2023fall\\python507\\homework\\final_project\\restaurants_data.json"

class SimpleCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def exists(self, key):
        return key in self.cache

app = Flask(__name__)
cache = SimpleCache()

YELP_API_KEY = 'TTgH2k2wHC1qad8-SfXCK6qS3Ipk6fsHb5pLwVPE16RHT4V1GHshCBE2Q8hAI5KoPyRkIpGqBZGxi6Ptku7trTwm6j_kbNiuKBXEgSAWm4_pKARGS74tUadF8LlzZXYx'
YELP_URL = 'https://api.yelp.com/v3/businesses/search'

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

@app.route('/download_json')
def download_json():
    try:
        return send_from_directory(DIRECTORY, 'restaurants_data.json', as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    
@app.route('/get_restaurants_data')
def get_restaurants_data():
    file_path = "C:\\Users\\mengfany\\Documents\\umich2023fall\\python507\\homework\\final_project\\restaurants_data.json"
    return send_file(file_path)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations')
def get_recommendations():
    cuisine = request.args.get('cuisine')
    location = request.args.get('location')
    price = request.args.get('price')
    rating = request.args.get('rating')
    cache_key = f"{cuisine}-{location}-{price}-{rating}"

    if cache.exists(cache_key):
        return render_template('recommendations.html', recommendations=cache.get(cache_key), source='cache')

    headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
    params = {'term': cuisine, 'location': location, 'price': price, 'limit': 6}

    response = requests.get(YELP_URL, headers=headers, params=params)
    if response.status_code == 200:
        restaurants = response.json()['businesses']
        cache.set(cache_key, restaurants)
        with open (json_file_path,'w') as file:
            json.dump(restaurants, file)
        return render_template('recommendations.html', recommendations=restaurants, source='Yelp API')
    else:
        return jsonify({'error': 'Error fetching data from Yelp'}), response.status_code

def build_graph_data_rating_similarity(restaurants, rating_threshold=0.5):
    nodes = [{'id': restaurant['id'], 'label': restaurant['name']} for restaurant in restaurants]
    edges = []

    for i, restaurant1 in enumerate(restaurants):
        for j, restaurant2 in enumerate(restaurants):
            if i < j: 
                if abs(restaurant1['rating'] - restaurant2['rating']) <= rating_threshold:
                    edges.append({'source': restaurant1['id'], 'target': restaurant2['id']})

    return {'nodes': nodes, 'edges': edges}

def build_graph_from_json():
    try:
        with open('restaurants_data.json', 'r') as file:
            restaurants = json.load(file)
        return build_graph_data_rating_similarity(restaurants)
    except FileNotFoundError:
        return None

if __name__ == '__main__':
    app.run(debug=True)
