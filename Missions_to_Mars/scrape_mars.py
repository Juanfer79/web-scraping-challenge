
#import Dependencies
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd

# SCRAPING 

# Define function to run all scraping

def scrape():

    # Dictionary creation to retaion variables 
    mars_dict = {}

    # Scrape 1 : Nasa Mars News

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("div", class_="content_title").a.text.strip('\n')
    news = soup.find('div', class_='rollover_description_inner').text.strip('\n')

    print("Nasa Mars News")
    print("-------------------------")
    print(title)
    print(news)

    # variables into dictionary
    mars_dict["title"] = title
    mars_dict["newsp"] = news

    # Scrape 2 : Image with Splinter
    
    # splniter browser
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    
    # launch splinter finder 
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    html2 = browser.html
    soup2 = BeautifulSoup(html2, "html.parser")
    # Find link
    featured_image = soup2.find("a",class_="button fancybox").get("data-fancybox-href")
    # print addresss
    featured_image_url="https://www.jpl.nasa.gov"+featured_image
    print("Mars Nasa Featured Image")
    print("-------------------------")
    print(featured_image_url)

    mars_dict["featured_image_url"] = featured_image_url

    # Scrape 3 : Weather Tweets 
    
    browser.visit("https://twitter.com/marswxreport?lang=en")
    
    browser.execute_script("window.scrollTo(2, document.body.scrollHeight);")
    html3 = browser.html
    soup3 = BeautifulSoup(html3, "html.parser")
    mars_tweets=""
    mars_weather_scrape = soup3.find_all("div", class_="css-901oao")
    for tweet in mars_weather_scrape:
            if "º" in tweet.text:
                mars_tweets = tweet.text
                break
    print("Mars Weather latest Tweet")
    print("-------------------------")
    print(mars_tweets)
    print()

    mars_dict["mars_tweets"] = mars_tweets


    # Scrape 4 : Mars Facts
    url4 = "https://space-facts.com/mars/"

    facts = pd.read_html(url4)[0]
    facts = facts.to_html(classes="table")

    print("Mars Facsts")
    print("-------------------------")
    print(facts)

    mars_dict["facts"] = facts

    # Scrape 5 : Mars Hemispheres Pictures 
    
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    response=requests.get(url)
    soup5=BeautifulSoup(response.text,"html.parser")
    hemi_text=soup5.find_all("div",class_="item")
    hemisphere_image_urls=[]
    for i in hemi_text:
        string=i.a.img["src"]
        desc=i.div.h3.text.rstrip(" Enhanced")
        hemisphere_image_urls.append(
        {
            "Desc":desc,
            "URL":f"https://astrogeology.usgs.gov/{string}"
        }
        )

    #create Dictrionary
    
    print("Mars Hemispheres Pictures Links")
    print("-------------------------")
    print(hemisphere_image_urls)

    mars_dict["hemisphereimg"] = hemisphere_image_urls

    # Close browser
    browser.quit()

    return mars_dict



    