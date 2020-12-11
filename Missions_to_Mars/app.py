from flask import Flask,render_template,Markup
import pymongo
import scrape_mars

app=Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

@app.route("/")
def index():
    mars_db=db.mars.find_one()
    return render_template("index.html",mars_dict=mars_db)

@app.route("/scrape")
def scraper():
    db.mars.drop()
    mars_db=scrape_mars.scrape()
    print(mars_db)
    print(type(mars_db))
    #db.mars.insert(mars_db.to_dict(orient="records"))
    db.mars.insert(mars_db)
    return render_template("index.html", mars_dict=mars_db)

if __name__ == "__main__":
    app.run(debug=True)