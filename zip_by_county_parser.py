from bs4 import BeautifulSoup
import pickle


def parse(county_page_html):
    soup = BeautifulSoup(county_page_html, 'html5lib')
    block = soup.div(class_='zsg-lg-1-2 zsg-sm-1-1')[0]
    lis = block.find_all("a")
    return [k.text for k in lis]


with open("county_page_source_dict.pickle", "rb") as f:
    county_page_source_dict = pickle.load(f)

county_zip_dict = {}
for county in county_page_source_dict.keys():
    county_zip_dict[county] = parse(county_page_source_dict[county])

with open("county_zip_dict.pickle", "wb") as f:
    pickle.dump(county_zip_dict, f)
