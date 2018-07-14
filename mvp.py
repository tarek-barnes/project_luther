from bs4 import BeautifulSoup
import json
import os
import pickle

def get_html(file_name):
    with open(file_name, "r") as f:
        html = f.read()
        f.close()
    return html

#  step 1: load html data from zip filenames
zip_codes = ['94102','94103','94104','94105','94107','94108','94109','94112','94114','94117']

with open("zip_coverage_dict.pickle", "rb") as f:
    zip_coverage_dict = pickle.load(f)

#  Create dict[zip_code] -> [html_p1, html_p2, ...]
my_dict = {}
for zip_code in zip_codes:
    n = zip_coverage_dict[zip_code]
    file_names = [zip_code+'_{}.txt'.format(k) for k in range(1, (n+1))]
    my_dict[zip_code] = []
    for file_name in file_names:
        my_dict[zip_code].append(get_html(file_name))



#  step 2: parse data, create df

# def parse_entry(html):
#     soup = BeautifulSoup(html, 'html5lib')
#     features = [k for k in soup.find_all("div", class_='minibubble template hide')]
#     features = [str(k) for k in features]
#     features = [k[(k.index("{")):] for k in features]
#     features = [k[:(k.rindex("}"))] for k in features]
#     features = features[1:-1]
#     features = [k.split(",") for k in features]
#     features = [k for k in features if len(k) > 50]
#     keywords = ["sqft", "streetAddress", "zipcode", "city", "price", "bathrooms", "bedrooms", "livingArea", "yearBuil", "lotSize", "homeType", "homeStatus", "daysOnZillow", "zestimate"]
#     repo = []
#     for feature in features:
#         my_list = []
#         for item in feature:
#             for key in keywords:
#                 if (key in item):
#                     my_list.append(item)
#         my_list = [k.split(":") for k in my_list]
#         repo.append(my_list)
#     return repo


def parse_entry(html):
    soup = BeautifulSoup(html, 'html5lib')
    features = [k for k in soup.find_all("div", class_='minibubble template hide')]
    features = [str(k) for k in features]
    features = [k[(k.index("{")):] for k in features]
    features = [k[:(k.rindex("}") + 1)] for k in features]
    features = [k.replace("\\", "") for k in features]
    features = [json.loads(k) for k in features]
    return features


def get_all_parsed_entries():
    all_html = []
    for zip_code in zip_codes:
        values = my_dict[zip_code]
        for k in range(len(values)):
            all_html.append(values[k])

    all_parsed_html = []
    for html in all_html:
        all_parsed_html+=parse_entry(html)

    return all_parsed_html


def get_prices(parsed_entries):
    prices = []
    for k in parsed_entries:
        for item in k:
            if item[0] == '"price"':
                prices.append(item[1].strip())
    return prices


def get_sqft(parsed_entries):
    sqft = []
    for k in parsed_entries:
        for item in k:
            if item[0] == '"sqft"':
                sqft.append(item[1].strip())
    return sqft


def get_bedrooms(parsed_entries):
    bedrooms = []
    for k in parsed_entries:
        for item in k:
            if item[0] == '"bedrooms"':
                bedrooms.append(item[1].strip())
    return bedrooms



def get_bathrooms(parsed_entries):
    bathrooms = []
    for k in parsed_entries:
        for item in k:
            if item[0] == '"bathrooms"':
                bathrooms.append(item[1].strip())
    return bathrooms


def get_livingarea(parsed_entries):
    living_area = []
    for k in parsed_entries:
        for item in k:
            if item[0] == '"livingArea"':
                living_area.append(item[1].strip())
    return living_area



def get_lotsize(parsed_entries):
    lot_size = []
    for k in parsed_entries:
        for item in k:
            if item[0] == '"lotSize"':
                lot_size.append(item[1].strip())
    return lot_size


all_parsed_entries = get_all_parsed_entries()
prices = get_prices(all_parsed_entries)
sqft = get_sqft(all_parsed_entries)
bedrooms = get_bedrooms(all_parsed_entries)
bathrooms = get_bathrooms(all_parsed_entries)
living_area = get_livingarea(all_parsed_entries)
lot_size = get_lotsize(all_parsed_entries)
