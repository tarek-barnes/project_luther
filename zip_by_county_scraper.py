# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
# import requests

#  This are the nine counties which make the SF Bay Area
bayarea_counties = ["Alameda",
                    "Contra Costa",
                    "Marin",
                    "Napa",
                    "San Francisco",
                    "San Mateo",
                    "Santa Clara",
                    "Solano",
                    "Sonoma"]

#  Get the URLs for Zillow pages which list ZIPs by county
bayarea_urls = [("https://www.zillow.com/browse/homes/ca/"+"{}-county".format(k)) for k in bayarea_counties]
bayarea_urls = [k.lower().replace(" ", "-")) for k in bayarea_counties]

county_url_dict = dict(zip(bayarea_counties, bayarea_urls))
county_page_source_dict = {}

chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)

#  Grab the list of ZIP codes from each county page
for county in county_url_dict.keys():
    url = county_url_dict[county]
    driver.get(url)
    page_source = driver.page_source
    county_page_source_dict[county] = page_source

with open("county_page_source_dict.pickle", "wb") as f:
    pickle.dump(county_page_source_dict, f)
