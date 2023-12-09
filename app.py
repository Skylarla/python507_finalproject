from flask import Flask, request, jsonify, render_template
import requests

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommendations')
def get_recommendations():
    cuisine = request.args.get('cuisine')
    location = request.args.get('location')
    price = request.args.get('price')
    cache_key = f"{cuisine}-{location}-{price}"

    if cache.exists(cache_key):
        return render_template('recommendations.html', recommendations=cache.get(cache_key), source='cache')

    headers = {'Authorization': f'Bearer {YELP_API_KEY}'}
    params = {'term': cuisine, 'location': location, 'price': price, 'limit': 5}

    response = requests.get(YELP_URL, headers=headers, params=params)
    if response.status_code == 200:
        restaurants = response.json()['businesses']
        cache.set(cache_key, restaurants)
        return render_template('recommendations.html', recommendations=restaurants, source='Yelp API')
    else:
        return jsonify({'error': 'Error fetching data from Yelp'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
