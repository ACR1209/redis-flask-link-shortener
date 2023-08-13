from flask import render_template, request, redirect, url_for
from app import app
import redis
import string
import random

SHORT_URL_LEN = 6
HOST_NAME = "http://localhost:5000"

# Connect to Redis server
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(SHORT_URL_LEN))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = generate_short_url()

        # Store the mapping in Redis
        redis_client.set(short_url, original_url)

        return render_template('index.html', short_url=short_url, host_url = HOST_NAME)

    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_original_url(short_url):
    original_url = redis_client.get(short_url)

    if original_url:
        return redirect(original_url)
    else:
        return "Short URL not found", 404
