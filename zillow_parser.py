from bs4 import BeautifulSoup
import os


# #  this marks pages with results as having no results
# def has_no_results(zip_code_page_source):
#     soup = BeautifulSoup(zip_code_page_source, 'html5lib')
#     if zip_code_page_source.find("Zillow has 0 homes for sale"):# or soup.find_all("div", id="map-result-count-message")[0].text == "No Results":
#         return 1


def has_no_results(zip_code_page_source):
    soup = BeautifulSoup(zip_code_page_source, 'html5lib')
    try:
        no_results = soup.find_all("h3")[0].text
        if no_results == 'No matching results...':
            return 1
        else:
            return 0
    except IndexError:
        return 0
