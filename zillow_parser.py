from bs4 import BeautifulSoup
import json
import os
import pickle


#  Get raw HTML from .txt files
def get_html(file_name):
    with open(file_name, "r") as f:
        html = f.read()
        f.close()
    return html



#  Turns an ugly string into a string that resembles a JSON
def parse_entry(html):
    soup = BeautifulSoup(html, 'html5lib')
    features = [k for k in soup.find_all("div", class_='minibubble template hide')]
    features = [str(k) for k in features]
    features = [k[(k.index("{")):] for k in features]
    features = [k[:(k.rindex("}") + 1)] for k in features]
    features = [k.replace("\\", "") for k in features]
    features = [json.loads(k) for k in features]
    return features



#  Create dict[zip_code] -> [html_p1, html_p2, ...]
def get_zip_html_dict():
    with open("zip_coverage_dict.pickle", "rb") as f:
        zip_coverage_dict = pickle.load(f)

    zip_codes = zip_coverage_dict.keys()
    zip_html_dict = {}
    for zip_code in zip_codes:
        n = zip_coverage_dict[zip_code]
        file_names = [zip_code+'_{}.txt'.format(k) for k in range(1, (n+1))]
        zip_html_dict[zip_code] = []
        for file_name in file_names:
            zip_html_dict[zip_code].append(get_html(file_name))

    return zip_html_dict



#  Turns a list of lists into a flattened list
def flatten(nested_list):
    return [k for sub_list in nested_list for k in sub_list]



#  Parse HTML into workable data
def get_zip_entries_dict():
    zip_html_dict = get_zip_html_dict()
    nested_dict = {key: flatten(list(map(parse_entry, zip_html_dict[key]))) for key in zip_html_dict}
    return nested_dict


#  Filters out values containing homeInfo from the JSON, which has the majority of useful features
def get_homeinfo_zip_entries_dict():
    zip_entries_dict = get_zip_entries_dict()
    return {key: [k for k in zip_entries_dict[key] if 'homeInfo' in k] for key in zip_entries_dict}



#  Returns a dict which has values containing all features needed (can be modified if I need more features)
def get_normalized_entries_dict():
    #  Cross-references features with items in the dictionary and keeps the overlap
    def cherry_pick_values(values):
        cherry_picked_values = []
        features = ['zipcode', 'latitude', 'longitude', 'price', 'yearBuilt', 'livingArea', 'lotSize', 'homeType', 'daysOnZillow']
        features = set(features)
        if len(values) > 0:
            for value in values:
                if set(value['homeInfo'].keys()) & features == features:
                    cherry_picked_values.append(value)
        return cherry_picked_values
    with open("homeinfo_zip_entries_dict.pickle", "rb") as f:
        homeinfo_zip_entries_dict = pickle.load(f)
    return {key: cherry_pick_values(homeinfo_zip_entries_dict[key]) for key in homeinfo_zip_entries_dict}



#  Creates a list of tuple entries for all ZIP codes
def get_entries_list(zip_code):
    normalized_entries_dict = get_normalized_entries_dict()
    zip_code_values = normalized_entries_dict[zip_code]
    final_entries = []
    if len(zip_code_values) > 0:
        for value in zip_code_values:
            bedrooms = value["bed"]
            bathrooms = value["bath"]
            square_feet = value["sqft"]
            latitude = value["homeInfo"]["latitude"]
            longitude = value["homeInfo"]["longitude"]
            price = value["homeInfo"]["price"]
            living_area = value["homeInfo"]["livingArea"]
            lot_size = value["homeInfo"]["lotSize"]
            home_type = value["homeInfo"]["homeType"]
            days_on_zillow = value["homeInfo"]["daysOnZillow"]
            year_built = value["homeInfo"]["yearBuilt"]

            final_entries.append((zip_code,
                                  price,
                                  home_type,
                                  square_feet,
                                  bedrooms,
                                  bathrooms,
                                  living_area,
                                  lot_size,
                                  latitude,
                                  longitude,
                                  days_on_zillow,
                                  year_built))
    return final_entries



#  Maps relevant tuple entries to a dict of counties where keys are counties and values are relevant entries
def get_county_entries_dict():
    with open("county_zip_dict.pickle", "rb") as f:
        county_zip_dict = pickle.load(f)
    return {county: flatten(list(map(get_entries_list, county_zip_dict[county]))) for county in county_zip_dict}



#  homeinfo_zip_entries_dict can be compiled inside get_county_entries_dict BUT it takes forever..
homeinfo_zip_entries_dict = get_homeinfo_zip_entries_dict()
with open("homeinfo_zip_entries_dict.pickle", "rb") as f:
    pickle.dump(homeinfo_zip_entries_dict, f)
