from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
from os.path import join, dirname
from dotenv import load_dotenv
import sys
import os
import random
import flask
import json
import requests


dotenv_path = join(dirname(__file__), 'tweet.env')
load_dotenv(dotenv_path)

consumer_key=os.environ["CONS_KEY"]
consumer_secret=os.environ["CONS_SECRET"]
access_token=os.environ["ACCESS_TOK"]
access_token_secret=os.environ["ACCESS_TOK_SEC"]
spoonacular_key = os.environ['SPOONACULAR_KEY']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


    
app = flask.Flask(__name__)

@app.route("/") #Python Decorator
def index():
    rands = random.randint(1,11) - 1
    
    foods = ["Lobster", "Ravioli", "Ziti", "Lasagna", "Donuts", "Mashed Potatoes", "Plantains", "Brownies", "Chocolate", "Spaghetti", "Rice"]
    
    #Twitter API
    
    tweets = Cursor(auth_api.search, q=foods[rands], lang="en").items(10)
    
    end_date = datetime.utcnow() - timedelta(days=30)
    
    source_url = []
    created_at = []
    screen_name = []
    ftweet = []
    
    #Spoonacular API
    
    ingredients = []
    
    url = "https://api.spoonacular.com/recipes/search?query={}&apiKey={}".format(foods[rands],spoonacular_key)
    response = requests.get(url)
    json_body = response.json()
    
    foodTitle = json_body["results"][0]["title"]
    foodReadyIn = json_body["results"][0]["readyInMinutes"]
    foodServings = json_body["results"][0]["servings"]
    foodURL = json_body["results"][0]["sourceUrl"]
    
    url = "https://api.spoonacular.com/recipes/{}/ingredientWidget.json?apiKey={}".format(json_body["results"][0]["id"],spoonacular_key)
    response = requests.get(url)
    json_body = response.json()
    for ingredient in json_body["ingredients"]:
        ingredients.append(ingredient["name"])
    
    for info in tweets:
        if info.created_at < end_date:
            break
        created_at.append(info.created_at)
        screen_name.append(info.user.screen_name)
        ftweet.append(info.text)
        source_url.append(info.id)

    return flask.render_template(
        "index.html",
        food = foods[rands],
        len = len(screen_name),
        created_at = created_at,
        screen_name = screen_name,
        ftweet = ftweet,
        source_url = source_url,
        foodTitle = foodTitle,
        foodReadyIn = foodReadyIn,
        foodServings = foodServings,
        foodURL = foodURL,
        ingredients = ingredients,
        ingLen = len(ingredient)

        )
    

app.run(
    port = int(os.getenv("PORT", 8080)),
    host = os.getenv("IP", "0.0.0.0")    
)
