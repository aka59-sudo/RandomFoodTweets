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


dotenv_path = join(dirname(__file__), 'tweet.env')
load_dotenv(dotenv_path)

consumer_key=os.environ["CONS_KEY"]
consumer_secret=os.environ["CONS_SECRET"]
access_token=os.environ["ACCESS_TOK"]
access_token_secret=os.environ["ACCESS_TOK_SEC"]

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)


    
app = flask.Flask(__name__)

@app.route("/") #Python Decorator
def index():
    rands = random.randint(1,10)

    foods = ["Lobster", "Crayfish", "Ziti", "Lasagna", "Quiche", "Mashed Potatoes", "Chicken Alfredo", "Brownies", "Chocolate", "Spaghetti", "Garlic Bread"]
    
    tweets = Cursor(auth_api.search, q=foods[rands], lang="en").items(10)
    
    end_date = datetime.utcnow() - timedelta(days=30)
    
    source_url = []
    created_at = []
    screen_name = []
    ftweet = []
    
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
        source_url = source_url
        
        )
    

app.run(
    port = int(os.getenv("PORT", 8080)),
    host = os.getenv("IP", "0.0.0.0")    
)
