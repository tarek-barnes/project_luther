from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import math
import numpy as np
import os
import pickle
import requests
import time

chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)


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


def get_pages_html(zip_codes):
    def is_multiple_pages(zip_code_page_source):
        try:
            stop = zip_code_page_source.find("homes for sale")
            start = zip_code_page_source.find("Zillow has") + len("Zillow has")
            num_str = page_source[start:stop].strip()
            num_pages = math.ceil(int(num_str) / 25)
            return (num_pages - 1)
        except NameError:
            return 0


    def get_other_page_urls(zip_code, num_pages):
        form = 'https://www.zillow.com/homes/{}_rb/{}_p/'
        page_nums = list(range(2, (num_pages + 1)))
        return [form.format(zip_code, p) for p in page_nums]


    def save(zip_code):
        zip_coverage_dict[zip_code] = len(zip_dict[zip_code])
        with open("zip_coverage_dict.pickle", "wb") as f:
            pickle.dump(zip_coverage_dict, f)

        n = zip_coverage_dict[zip_code]
        pages = list(range(n))
        txt_names = [(zip_code+"_"+str(p+1)+".txt") for p in pages]

        for page in pages:
            relevant_html = zip_dict[zip_code][page]
            with open((txt_names[page]), "w") as f:
                f.write(relevant_html)
                f.close()



    zillow_url = "https://www.zillow.com/buy/"
    driver.get(zillow_url)
    zip_dict = {}
    try:
        with open("zip_coverage_dict.pickle", "rb") as f:
            zip_coverage_dict = pickle.load(f)
    except FileNotFoundError:
        zip_coverage_dict = {}

    for zip_code in zip_codes:
        if zip_code in zip_coverage_dict:
            continue
        else:
            search_box = driver.find_element_by_xpath("//input[@id='citystatezip']")
            time.sleep(np.random.poisson(30))
            search_box.clear()
            search_box.click()
            search_box.send_keys(zip_code)
            search_button = driver.find_element_by_xpath("//button[@type='submit']")
            time.sleep(np.random.poisson(20))
            search_button.click()
            page_source = driver.page_source
            zip_dict[zip_code] = [page_source]

            if has_no_results(page_source):
                zip_coverage_dict[zip_code] = 0
                with open("zip_coverage_dict.pickle", "wb") as f:
                    pickle.dump(zip_coverage_dict, f)
                continue

            elif is_multiple_pages(page_source):
                other_urls = get_other_page_urls(zip_code, (is_multiple_pages(page_source) + 1))
                for other_url in other_urls:
                    time.sleep(np.random.poisson(42))
                    zillow_url = other_url
                    driver.get(zillow_url)
                    other_html = driver.page_source
                    zip_dict[zip_code].append(other_html)
                save(zip_code)

            else:
                save(zip_code)

        time.sleep(np.random.poisson(59))
        driver.execute_script("window.history.go(-1)")
    driver.close()
    return zip_dict



# starting with SF!

zip_codes = ['94588',
 '94587',
 '94601',
 '94603',
 '94602',
 '94605',
 '94607',
 '94606',
 '94609',
 '94608',
 '94611',
 '94610',
 '94613',
 '94612',
 '94618',
 '94619',
 '94621',
 '94660',
 '94661',
 '94701',
 '94703',
 '94702',
 '94501',
 '94705',
 '94704',
 '94707',
 '94502',
 '94706',
 '94709',
 '94708',
 '94710',
 '94720',
 '94514',
 '94536',
 '94538',
 '94540',
 '94539',
 '94542',
 '94541',
 '94544',
 '94546',
 '94545',
 '94552',
 '94551',
 '94555',
 '94560',
 '94566',
 '94568',
 '94577',
 '95391',
 '94579',
 '94578',
 '94580',
 '94586',
 '94903',
 '94901',
 '94904',
 '94920',
 '94925',
 '94924',
 '94929',
 '94930',
 '94937',
 '94933',
 '94939',
 '94938',
 '94941',
 '94940',
 '94947',
 '94946',
 '94949',
 '94948',
 '94950',
 '94957',
 '94956',
 '94963',
 '94960',
 '94965',
 '94964',
 '94970',
 '94971',
 '94973']


get_pages_html(zip_codes)





# EXPERIMENTING!
#
# soup = BeautifulSoup(page_source, 'html5lib')
# [e for e in soup.find_all('h2')][0].text
#
#
# len([e for e in soup.find_all('a', class_='zsg-photo-card-overlay-link')])
#
#
# len([k for k in soup.find_all("div", class_='minibubble template hide')])
