from flask import Flask, render_template, redirect, url_for, Markup
import pymongo
import scrape_mars

app = Flask(__name__)

# connect database
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
database = client.mars_database


@app.route("/")
def index():
    marsdb_dict = {}
    marsdb_dict = db.mars_dict.find_one()
    is_empty=False

    # Check if it is the first time so the dictionary doesn't have any information
    if not bool(marsdb_dict):
        is_empty = True
        print ("Dictionary is Empty")

    return render_template("index.html", mars=marsdb_dict, is_empty=is_empty)

@app.route("/scrape")
def scrape():
    # call the function on the scrape_mars.py
    marsdb_dict = scrape_mars.scrape()
    # clean the collection
    db.mars_dict.drop()
    # save it in MongoDB
    db.mars_dict.insert(marsdb_dict)

    return render_template("index.html", mars=marsdb_dict)
    #return redirect(url_for("index", mars=mars_dict))


if __name__ == "__main__":
    app.run(debug=True)