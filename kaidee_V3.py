import sys
import os
import requests
import codecs
import re
import json
import argparse
import pandas as pd
import reic_function as fn
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint, randrange
from datetime import datetime,timedelta
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
import cloudscraper
import platform
import time
import ssl

# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

web = "kaidee"
# base_url = "https://baan.kaidee.com/placeholder_property_sell_rentplaceholder_type/p-placeholder_page/?condition=2&sort=latest"
base_url = "https://baan.kaidee.com/placeholder_type/p-placeholder_page?condition=2&sort=latest"
# https://baan.kaidee.com/c15-realestate-home/p-2?condition=2&sort=latest
date_now = fn.get_date_now()
date = datetime(2025, 8, 29).strftime('%Y-%m-%d')
property_type = {
    "home"          : {"type_id": 1, "route": "c15-realestate-home", "property_sell_rent": "", "start": 1, "end": 24},
    "condo"         : {"type_id": 2, "route": "c17-realestate-condo", "property_sell_rent": "", "start": 1, "end": 72},
    "townhouse"     : {"type_id": 3, "route": "c16-realestate-townhouse", "property_sell_rent": "", "start": 1, "end": 22}
    # "home_rent"     : {"type_id": 1, "route": "c15-realestate-home", "property_sell_rent": "for-rent/", "start": 1, "end": 2},
    # "condo_rent"    : {"type_id": 2, "route": "c17-realestate-condo", "property_sell_rent": "for-rent/", "start": 1, "end": 2},
    # "townhouse_rent": {"type_id": 3, "route": "c16-realestate-townhouse", "property_sell_rent": "for-rent/", "start": 1, "end": 2}
}


# ++++++++++++ CloudScraper +++++++++++++++++
rand = randint(1000, 10000)
browsers = ['chrome', 'firefox']
platforms = [{'platform': 'linux', 'mobile': False, 'desktop': True},
             {'platform': 'windows', 'mobile': False, 'desktop': True},
             {'platform': 'darwin', 'mobile': False, 'desktop': True},
             {'platform': 'android', 'mobile': True, 'desktop': False}]

rand_browser = browsers[randint(0, 1)]
rand_platform = platforms[randint(0, 3)]

scraper = cloudscraper.create_scraper(
    browser={
        'browser': rand_browser,
        'platform': rand_platform['platform'],
        'desktop': rand_platform['desktop'],
        'mobile': rand_platform['mobile']
    },
    delay=rand,
    interpreter='nodejs',
)
thai_full_months = [
    'มกราคม',
    'กุมภาพันธ์',
    'มีนาคม',
    'เมษายน',
    'พฤษภาคม',
    'มิถุนายน',
    'กรกฎาคม',
    'สิงหาคม',
    'กันยายน',
    'ตุลาคม',
    'พฤศจิกายน',
    'ธันวาคม',
]
thai_abbr_months = [
        "ม.ค.",
        "ก.พ.",
        "มี.ค.",
        "เม.ย.",
        "พ.ค.",
        "มิ.ย.",
        "ก.ค.",
        "ส.ค.",
        "ก.ย.",
        "ต.ค.",
        "พ.ย.",
        "ธ.ค.",
]

if not os.path.isdir("links/" + date):
    os.mkdir("links/" + date)
path_links = "links/" + date + "/" + web
if not os.path.isdir(path_links):
    os.mkdir(path_links)
if not os.path.isdir('Files/' + date):
    os.mkdir('Files/' + date)
path_Files = 'Files/' + date + '/' + web
if not os.path.isdir(path_Files):
    os.mkdir(path_Files)


ids = []
webs = []
names = []
house_pictures = []
project_names = []
addresss = []
province_codes = []
district_codes = []
sub_district_codes = []
prices = []
range_of_house_prices = []
area_SQMs = []
area_SQWs = []
floor_numbers = []
floors = []
sell_type_ids = []
source_ids = []
bedrooms = []
bathrooms = []
garages = []
details = []
latitudes = []
longtitudes = []
duplicates = []
news = []
cross_webs = []
cross_refs = []
completion_years = []
days = []
months = []
years = []
post_dates = []
seller_names = []
seller_tels = []
seller_emails = []
seller_ids = []
room_numbers = []
house_links = []
type_ids = []
date_times = []

def get_data_datetime(soup_txt,_dateF=False):
    if _dateF:
        day = soup_txt.split(" ")[0]
        month = soup_txt.split(" ")[1]
        year = str(int(soup_txt.split(" ")[2]) - 543)
        if month in thai_abbr_months:
            month = str(thai_abbr_months.index(month)+1)
        else:
            if month in thai_full_months:
                month = str(thai_full_months.index(month)+1)
            else:
                month = "None"
        if month != "None":
            if len(month) == 1:
                month = "0" + month
        return day,month,year


def get_data(prop_url,type_id,scraper):
    # print(prop_url)
    Headers = {'User-Agent': ua.random}
    print(Headers)
    # req = requests.get(prop_url, headers=Headers)
    req = scraper.get(prop_url, headers=Headers)

    print(req.status_code)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')
    wait_time = 2.0
    sleep(wait_time)

    # scripts = soup.find_all('script')
    # print(scripts)
    # for script in scripts:
    #     if '<script type="application/ld+json">' in str(script):
    #         temp = json.loads(str(script).replace('<script type="application/ld+json">', '').replace('</script>', ''))
            # print(temp)
            # if temp["@type"] == "Product":
            #     data = temp
                # print(data)

    try:
        webs.append(web)
        project_names.append("none")
        _o = int(0)

        try:
            _names = soup.find('h1', class_='sc-747m9u-7 cJvkVk').get_text()
            print(_names)
            # _names = data["name"]
            names.append(_names)
        except Exception as err:
            names.append("none")

        try:
            _address = soup.find('span', class_='sc-3tpgds-0 kBbZux sc-mj06cq-1 biQatR').parent.parent.get_text()\
                         .split('ตำแหน่ง')[1].split('หมายเลข')[0]
            _locationss =  _address.split()
            _province_codes  = _locationss[1]
            _district_codes =  _locationss[0]
            _sub_district_codes = "none"
            _prv, _dis, _subdis = fn.prov_dis_subdis(_province_codes,_district_codes,_sub_district_codes)
            addresss.append(_address)
            province_codes.append(int(_prv))
            district_codes.append(int(_dis))
            sub_district_codes.append(int(_subdis))
            # print(district_codes)

        except Exception as err:
            addresss.append('none')
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')

        # try:
        #     _prv, _dis, _subdis = fn.prov_dis_subdis(_address[2], _address[1], _address[0])
        #     province_codes.append(int(_prv))
        #     district_codes.append(int(_dis))
        #     sub_district_codes.append(int(_subdis))
        # except Exception as err:
        #     province_codes.append('none')
        #     district_codes.append('none')
        #     sub_district_codes.append('none')
        #     # print('Error => prv')
        #
        try:
            # _prices = soup.find('span', class_='sc-3tpgds-0 cssmeV').get_text()
            _prices = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())['props']['pageProps']['adDetail']\
                           ['ad']['price']
            # _prices = soup.find('div', class_='sc-12ljfib-0 eKqAFc sc-1lmqj83-0 iMUPwp')
            # print(_prices)
            # print(_prices)
            # _price = data["offers"][0]["price"]
            prices.append(_prices)
            range_of_house_prices.append(fn.get_range_of_price(int(_prices)))
            # print(range_of_house_prices)
            # print(range_of_house_prices)
        except Exception as err:
            prices.append(_o)
            range_of_house_prices.append(9)
        #
        try:
            _bedrooms = soup.find('ul', class_='sc-z3mufy-2 htYEwh').get_text().split('นอน')[1].replace('ห้อง','').split('น้ำ')[0].strip()
            # print(_bedrooms)
            # _bedrooms = soup.find('span', {'class': 'cfe8d274', 'aria-label': 'Beds'}).get_text().strip().replace(' ห้องนอน', '')
            bedrooms.append(int(_bedrooms))
        except Exception as err:
            bedrooms.append('none')
        #
        try:
            _bathrooms =soup.find('ul', class_='sc-z3mufy-2 htYEwh').get_text().split('น้ำ')[1].replace('ห้อง','').strip()
            # print(_bathrooms)
            # _bathrooms = soup.find('span', {'class': 'cfe8d274', 'aria-label': 'Baths'}).get_text().strip().replace(' ห้องน้ำ', '')
            bathrooms.append(int(_bathrooms))
        except Exception as err:
            bathrooms.append('none')
        #
        try:
            _area = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())['props']['pageProps']['adDetail']\
                           ['ad']['attributes'][0]['value'].split('.')[0]
            # print(_area)
            if type_id == 2:
                area_SQWs.append(int(_area) * 4)
                # print(area_SQWs)
                area_SQMs.append(int(_area))
                # print(area_SQWs)
                # print(area_SQMs)
            else:
                area_SQWs.append(int(_area))
                area_SQMs.append(int(_area) * 4)

        except Exception as err:
            area_SQWs.append('none')
            area_SQMs.append('none')


        try:
            _detail = soup.find('p', class_='inner-text').get_text().strip()
            # print(_detail)
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _picture =json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())['props']['pageProps']['adDetail']\
                           ['ad']['images'][0]['sizes']['large']['link']
            # print(_picture)
            # _picture = soup.find('div', class_='sc-aicb4t-0 ieiBqw').find('picture', class_='sc-27ozv5-1 gAHpMv').find('source')['data-src']
            # print(_picture)
            # _picture = data["image"][0]
            house_pictures.append(_picture)
        except Exception as err:
            house_pictures.append('none')
        #
        try:
            source_ids.append(int(fn.get_source_id(web)))
        except Exception as err:
            source_ids.append(_o)

        try:
            _seller_names = soup.find('span', class_='sc-3tpgds-0 vqCwQ sc-1k125n6-0 kJVXWX').get_text().strip()
            # print(_seller_names)
            seller_names.append(_seller_names)
        except Exception as err:
            seller_names.append("none")

        try:
            _seller_tels = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())['props']['pageProps']['adDetail']\
                           ['ad']['member']["telephone"]
            # _seller_tels1 =_seller_tels["telephone"]
            # print(_seller_tels)
            # _seller_tels = data["offers"][0]["offeredBy"]["telephone"]
            seller_tels.append(_seller_tels)
        except Exception as err:
            seller_tels.append("none")

        try:
            _seller_emails = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())['props']['pageProps'][
                'adDetail']['ad']['member']["email"]
            # _seller_tels1 =_seller_tels["telephone"]
            # print(_seller_emails)
            # _seller_tels = data["offers"][0]["offeredBy"]["telephone"]
            seller_emails.append(_seller_emails)
        except Exception as err:
            seller_emails.append("none")

        try:
            _map = _seller_tels = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())['props']['pageProps']['adDetail']\
                           ['ad']['locations'][0]
            # print(_map)
            _latitudes = _map['latitude']
            _longtitudes = _map['longitude']
            latitudes.append(_latitudes)
            longtitudes.append(_longtitudes)

        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')

        try:
            if property_type[prop_type]["property_sell_rent"] == "for-rent/":
                _sell_type_ids = int(2)
            else:
                _sell_type_ids = int(1)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))

        floor_numbers.append('none')
        # prices.append('none')
        # range_of_house_prices.append('none')
        floors.append('none')
        days.append('none')
        months.append('none')
        years.append('none')
        post_dates.append('none')
        # seller_emails.append("none")
        seller_ids.append(_o)
        completion_years.append('none')
        room_numbers.append('none')
        garages.append('none')
        # latitudes.append('none')
        # longtitudes.append('none')
        duplicates.append(_o)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        house_links.append(prop_url)
        type_ids.append(type_id)
        date_times.append(date_now)

        print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)

    # sleep(randrange(2))


def loop_links(prop_type,scraper):
    file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        ids.append(ID)
        link = links[i]
        get_data(link.strip(), type_id,scraper)
        # break


def save_list_links(prop_type,scraper):
    print("---------------------::  " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    # list_type = property_type[prop_type]["property_sell_rent"]
    req_url = base_url.replace("placeholder_type", route)
        # .replace("placeholder_property_sell_rent", str(list_type))

    for i in tqdm(range(start_page, end_page)):
        Headers = {'User-Agent': ua.random}
        print(Headers)
        wait_time = 0.50
        url = req_url.replace("placeholder_page", str(i))
        # r = scraper.requests.get(url, headers=Headers)
        # print(r.status_code)
        # while r.status_code != 200:
        #     r = requests.get(url, headers=Headers)
        r = scraper.get(url, headers=Headers)
        print(r.status_code)
        # ใช้ scraper.get() แทน requests.get()
        while r.status_code != 200:
            r = scraper.get(url, headers=Headers)
        all_links = extract_links(r.text)
        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for link in all_links:
            file_links.writelines(link + "\n")
        file_links.close()
        sleep(wait_time)
#
def extract_links(content):
    links = []
    for i in list( dict.fromkeys(re.findall("product-\d{1,10}",content))):
        links.append("https://baan.kaidee.com/" + i)
    return links

if __name__ == '__main__':
    # Get link
    # for prop_type in property_type:
    #     save_list_links(prop_type,scraper)
      # break

    # Get Data
    #
    for prop_type in property_type:
        print("---------------------::  GET DATA " + prop_type + "  ::---------------------")
        loop_links(prop_type,scraper)
    # #     # break
    # #
    print('ids', len(ids))
    print('webs', len(webs))
    print('names', len(names))
    print('house_pictures', len(house_pictures))
    print('project_names', len(project_names))
    print('addresss', len(addresss))
    print('province_codes', len(province_codes))
    print('district_codes', len(district_codes))
    print('sub_district_codes', len(sub_district_codes))
    print('prices', len(prices))
    print('range_of_house_prices', len(range_of_house_prices))
    print('area_SQMs', len(area_SQMs))
    print('area_SQWs', len(area_SQWs))
    print('floor_numbers', len(floor_numbers))
    print('floors', len(floors))
    print('sell_type_ids', len(sell_type_ids))
    print('source_ids', len(source_ids))
    print('bedrooms', len(bedrooms))
    print('bathrooms', len(bathrooms))
    print('garages', len(garages))
    print('details', len(details))
    print('latitudes', len(latitudes))
    print('longtitudes', len(longtitudes))
    print('duplicates', len(duplicates))
    print('news', len(news))
    print('cross_webs', len(cross_webs))
    print('cross_refs', len(cross_refs))
    print('days', len(days))
    print('months', len(months))
    print('years', len(years))
    print('post_dates', len(post_dates))
    print('seller_names', len(seller_names))
    print('seller_tels', len(seller_tels))
    print('seller_emails', len(seller_emails))
    print('seller_ids', len(seller_ids))
    print('room_numbers', len(room_numbers))
    print('house_links', len(house_links))
    print('type_ids', len(type_ids))
    print('completion_years', len(completion_years))
    print('date_times', len(date_times))

    #
    property_list = pd.DataFrame({
        'ID': ids,
        'web': webs,
        'name': names,
        'project_name': project_names,
        'address': addresss,
        'subdistrict_code': sub_district_codes,
        'district_code': district_codes,
        'province_code': province_codes,
        'price': prices,
        'range_of_house_price': range_of_house_prices,
        'area_SQM': area_SQMs,
        'area_SQW': area_SQWs,
        'floor_number': floor_numbers,
        'floor': floors,
        'room_number': room_numbers,
        'bedroom': bedrooms,
        'bathroom': bathrooms,
        'garage': garages,
        'latitude': latitudes,
        'longtitude': longtitudes,
        'detail': details,
        'seller_name': seller_names,
        'seller_tel': seller_tels,
        'seller_email': seller_emails,
        'seller_id': seller_ids,
        'picture': house_pictures,
        'house_link': house_links,
        'type_id': type_ids,
        'sell_type_id': sell_type_ids,
        'source_id': source_ids,
        'duplicate': duplicates,  # 0
        'new': news,  # 1
        'cross_web': cross_webs,  # -1
        'cross_ref': cross_refs,  # str("None")
        'completion_year': completion_years,  # str("None")
        'year': years,
        'month': months,
        'day': days,
        'post_date': post_dates,
        'date_time': date_times,  # date
        'update_date': post_dates,
    })

    property_list.to_csv(path_Files + '/' + web + '.csv')
    print('Export', len(ids), 'Rows To CSV File Completed!!!! ')