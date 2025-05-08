import sys
import os
import requests
import codecs
import re
import json
# import pyautogui
import argparse
import webbrowser
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
from datetime import datetime,timedelta
from selenium import webdriver
import time
import geckodriver_autoinstaller
from fake_useragent import UserAgent
import platform
import ssl
import reic_function as fn

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

date = datetime(2025, 4, 30).strftime('%Y-%m-%d')
date_now = fn.get_date_now()
web = 'homemarket'
base_url = 'https://homehug.in.th/search?search=1&lat=15.90568418&lng=101.45705990&zoom=6&listingType=placeholder_sale_rent' \
           '&propertyType=placeholder_type&beds=0,1,2,3,4,5,6&baths=0,1,2,3,4,5,6'
# base_url = 'https://www.homehug.in.th/search?search=1&zoom=11&statusZoom=1&statusSearch=0&listingType=placeholder_sale_rent&propertyType=placeholder_type&beds=&baths=&minPrice=&maxPrice=&text='

property_type = {
    "home"          : {"type_id": 1, "route": "1", "property_sell_rent": 1, "start": 1, "end": 119},
    "condo"         : {"type_id": 2, "route": "2", "property_sell_rent": 1, "start": 1, "end": 69},
    "townhouse"     : {"type_id": 3, "route": "3", "property_sell_rent": 1, "start": 1, "end": 107},
    "home_rent"     : {"type_id": 1, "route": "1", "property_sell_rent": 2, "start": 1, "end": 38},
    "condo_rent"    : {"type_id": 2, "route": "2", "property_sell_rent": 2, "start": 1, "end": 30},
    "townhouse_rent": {"type_id": 3, "route": "3", "property_sell_rent": 2, "start": 1, "end": 21},
}

# base_url = 'https://www.homehug.in.th/placeholder_sale_rent-placeholder_type?beds=&baths=&minPrice=&maxPrice=&searchword='
#
#
#
# property_type = {
#     "home"          : {"type_id": 1, "route": "%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99", "property_sell_rent": "%E0%B8%82%E0%B8%B2%E0%B8%A2", "start": 1, "end": 1},
#     "condo"         : {"type_id": 2, "route": "%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B9%82%E0%B8%94", "property_sell_rent": "%E0%B8%82%E0%B8%B2%E0%B8%A2", "start": 1, "end": 1},
#     "townhouse"     : {"type_id": 3, "route": "%E0%B8%97%E0%B8%B2%E0%B8%A7%E0%B8%99%E0%B9%8C%E0%B9%82%E0%B8%AE%E0%B8%A1", "property_sell_rent": "%E0%B8%82%E0%B8%B2%E0%B8%A2", "start": 1, "end": 1},
#     "home_rent"     : {"type_id": 1, "route": "%E0%B8%9A%E0%B9%89%E0%B8%B2%E0%B8%99", "property_sell_rent": "%E0%B9%80%E0%B8%8A%E0%B9%88%E0%B8%B2", "start": 1, "end": 1},
#     "condo_rent"    : {"type_id": 2, "route": "%E0%B8%84%E0%B8%AD%E0%B8%99%E0%B9%82%E0%B8%94", "property_sell_rent": "%E0%B9%80%E0%B8%8A%E0%B9%88%E0%B8%B2", "start": 1, "end": 1},
#     "townhouse_rent": {"type_id": 3, "route": "%E0%B8%97%E0%B8%B2%E0%B8%A7%E0%B8%99%E0%B9%8C%E0%B9%82%E0%B8%AE%E0%B8%A1", "property_sell_rent": "%E0%B9%80%E0%B8%8A%E0%B9%88%E0%B8%B2", "start": 1, "end": 1},
# }


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
completion_years = []
date_times = []


def get_data(prop_url, type_id, ID = 0):
    # print(prop_url)
    Headers = {'User-Agent': ua.random}
    req = requests.get(prop_url, headers=Headers)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup)

    if soup.find('a', class_='btn-try') == None:

        try:
            ids.append(ID)
            webs.append(web)
            date_times.append(date_now)
            house_links.append(prop_url)
            type_ids.append(type_id)
            try:
                name = soup.find('title').get_text().split('|')[0].strip().replace(',', '')
                # print(name)
                names.append(name)
            except Exception as err:
                names.append('none')

            try:
                project_name = soup.find('h1', class_='title-unit mb-0').get_text().strip().replace(',', '')
                # print(project_name)

                project_names.append(project_name)

            except Exception as err:
                project_names.append('none')

            _location_detail = soup.find('div', id='detailUnit')
            try:
                _sub_district = _location_detail.find(text='แขวง/ตำบล').parent.parent.next_sibling.get_text()
            except Exception as err:
                _sub_district = 'none'

            try:
                _district = _location_detail.find(text='เขต/อำเภอ').parent.parent.next_sibling.get_text()
            except Exception as err:
                _district = 'none'

            try:
                _province = _location_detail.find(text='จังหวัด').parent.parent.next_sibling.get_text()
            except Exception as err:
                _province = 'none'

            try:
                addresss.append(_sub_district + ' ' + _district + ' ' + _province)
            except Exception as err:
                addresss.append('none')

            _prv_code, _dis_code, _subdis_code = fn.prov_dis_subdis(_province, _district, _sub_district)
            province_codes.append(_prv_code)
            district_codes.append(_dis_code)
            sub_district_codes.append(_subdis_code)

            try:
                # _price = soup.find('span', class_='mb-0 title-price').get_text().replace('฿', '').replace(',', '').strip()
                _price = int(re.sub('[^0-9]', '', soup.find('span', class_='mb-0 title-price').get_text().strip()))
                prices.append(_price)
                range_of_house_prices.append(fn.get_range_of_price(_price))
            except Exception as err:
                prices.append(0)
                range_of_house_prices.append(0)

            try:
                area_SQMs.append(
                    soup.find('div', class_='card-section1').find('p', class_='title-spec').get_text().strip())
            except Exception as err:
                area_SQMs.append('none')

            area_SQWs.append('none')
            room_numbers.append('none')

            try:
                seller_names.append(soup.find('a', class_='owner-name d-block font-prompt500').get_text())
            except Exception as err:
                seller_names.append('none')

            try:
                seller_tels.append(soup.find('p', class_='owner-phone').get_text())
            except Exception as err:
                seller_tels.append('none')

            seller_emails.append('none')
            # seller_id ยังไม่ได้ทำ รอคำตอบจาก RS ว่าได้ใช้งานหรือไม่
            seller_ids.append(0)
            sell_type_ids.append(1)

            try:
                bedrooms.append(soup.find('div', class_='card-section2').find('p', class_='title-spec').get_text())
            except Exception as err:
                bedrooms.append()

            try:
                bathrooms.append(soup.find('div', class_='card-section3').find('p', class_='title-spec').get_text())
            except Exception as err:
                bathrooms.append('none')

            garages.append('none')

            try:
                _detail = soup.find('div', class_='mt-3 raw-html').get_text().replace('\n', '').replace('\r',
                                                                                                        '').replace(',',
                                                                                                                    ' ')
                details.append(_detail)
            except Exception as err:
                details.append('none')

            # try:
            #     id = ID
            #     # ids.append(ID)
            #     ids.append(id if id else 'none')
            # except Exception as err:
            #     ids.append('none')

            latitudes.append('none')
            longtitudes.append('none')
            duplicates.append(0)
            news.append(1)
            cross_webs.append('none')
            cross_refs.append('none')
            floors.append('none')
            floor_numbers.append('none')

            try:
                _house_pictures = soup.find('div', class_='slick-active').find('img', class_='lazy')['data-src']
                if _house_pictures == '':
                    _house_pictures = 'none'
                house_pictures.append(_house_pictures if _house_pictures else 'none')
                # print(house_pictures)
            except Exception as err:
                house_pictures.append('none')
            # try:
            #     _div = soup.find('div', class_='slick-active')
            #     if _div:
            #         _img = _div.find('img', class_='lazy')
            #         _house_pictures = _img.get('data-src') if _img else None
            #         house_pictures.append(_house_pictures if _house_pictures else 'none')
            #     else:
            #         house_pictures.append('none')
            # except Exception as err:
            #     print(f"Error fetching house pictures: {err}")
            #     house_pictures.append('none')

            try:
                source_ids.append(fn.get_source_id('home'))
            except Exception as err:
                source_ids.append('none')

            # house_links.append(prop_url)
            # type_ids.append(type_id)
            completion_years.append('none')

            try:
                _post_date = soup.find(text='วันที่อัพเดตล่าสุด').parent.parent.next_sibling.get_text().split('-')
                _day = _post_date[0]
                _month = _post_date[1]
                _year = _post_date[2]
                days.append(_day)
                months.append(_month)
                years.append(_year)
                post_dates.append(str(_year) + '-' + str(_month) + '-' + str(_day))
            except Exception as err:
                days.append('none')
                months.append('none')
                years.append('none')
                post_dates.append('none')

            # ids.append(ID)
            # webs.append(web)
            # date_times.append(date_now)

            print('Get Data OK')
        except Exception as err:
            print('\n', prop_url)
            print('ERROR!!! =>', err)
            house_pictures.append('none')
            floor_numbers.append('none')
            floors.append('none')
            source_ids.append('none')
            bedrooms.append('none')
            bathrooms.append('none')
            garages.append('none')
            details.append('none')
            latitudes.append('none')
            longtitudes.append('none')
            duplicates.append('none')
            news.append('none')
            cross_webs.append('none')
            cross_refs.append('none')
            days.append('none')
            months.append('none')
            years.append('none')
            post_dates.append('none')
            completion_years.append('none')
    else:
        print('ERROR!!! \n', prop_url)

def loop_links(prop_type):
    file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        # ids.append(ID)
        link = links[i]
        try:
            get_data(link.strip(), type_id, ID)
        except Exception as err:
            print(err)
        # sleep(0.2)
        # break



def save_list_links(prop_type):
    print("---------------------::  GET LINK " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"] - 1
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    link_type = property_type[prop_type]["property_sell_rent"]

    for i in tqdm(range(start_page, end_page)):
        _skip = i * 32
        headers = {"Authorization": "ZGExMjFjOGZlMTRmNjI4NGY1ODA3ZjMyZjliMThjYTY3MzhhMTlmZQ==",
                   "Content-Type": "application/json",
                   "User-Agent": str(ua.random),
                   "Host": "searchapi.home.co.th",
                   "Origin": "https://www.homehug.in.th",
                   "Referer": "https://www.homehug.in.th/",
                   "Sec-Fetch-Dest": "empty",
                   "Sec-Fetch-Mode": "cors",
                   "Sec-Fetch-Site": "same-site"
                   }

        playload = '{"listingType":[' + str(link_type) + '],\
                       "propertyType":[' + str(route) + '],\
                       "minPrice":0,\
                       "maxPrice":0,\
                       "bath":[0,1,2,3,4,5,6],\
                       "bed":[0,1,2,3,4,5,6],\
                       "schWord":"",\
                       "provinceID":0,\
                       "districtID":0,\
                       "dbName":["homecontent"],\
                       "pageSize":32,\
                       "page":' + str(i) + ',\
                       "sourceId":""}'

        req = requests.post("https://searchapi.home.co.th/api/Listing", headers=headers, data=playload)
        _data = json.loads(req.text)

        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for i in _data['schMarket']:
            _link = 'https://market.home.co.th/realestate/' + i['title'].replace(' ', '-').replace('\n', '') + '-' + str(i['listingID'])
            file_links.writelines(_link + "\n")
        file_links.close()
        sleep(0.1)

if __name__ == "__main__":
    # GET LINK
    for prop_type in property_type:
        save_list_links(prop_type)
        # break

    # GET DATA
    for prop_type in property_type:
        print('\n', "---------------------::  GET DATA " + prop_type + "  ::---------------------")
        loop_links(prop_type)
        # break

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

    property_list.to_csv(path_Files + '/' + web + '_' + prop_type + '.csv')
    print('Export', len(ids), 'Rows To CSV File Completed!!!! ')
