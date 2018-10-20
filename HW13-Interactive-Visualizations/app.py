from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars
<<<<<<< HEAD
import os
from flask_pymongo import PyMongo

MONGO_URL = os.environ.get('MONGODB_URI')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/rest"
=======
>>>>>>> parent of d7d53ad... Update app.py to use Flask-PyMongo; those changes plus Procfile and requirements needed to deploy to Heroku

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.mars_facts
@app.route('/scrape')
def scrape():
    mars = scrape_mars.scrape()
    # print("\n\n\n")
    print(mars['featured_image_url'])
<<<<<<< HEAD
    # collection.insert_one(mars)
    mongo.db.mars_facts.insert(mars)
    return redirect("/", code=302)
=======
    collection.insert_one(mars)
    return redirect("http://localhost:5000/", code=302)
>>>>>>> parent of d7d53ad... Update app.py to use Flask-PyMongo; those changes plus Procfile and requirements needed to deploy to Heroku

@app.route("/")
def home():
    mars = list(db.mars_facts.find())
    print(mars[0]['featured_image_url'])
    return render_template("index.html", mars = mars[-1])

if __name__ == "__main__":
    app.run(debug=True)
