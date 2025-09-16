import sys
import os
import requests
import codecs
import re
import argparse
import pandas as pd
import reic_function as fn
import platform
import time
import ssl
import json
import pyautogui
import pyperclip
import random

import cloudscraper
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint, randrange
from datetime import datetime, timedelta
from random import randint
from fake_useragent import UserAgent
# from requests_html import HTMLSession


ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

# base_url = "https://tb.co.th/search?tx=full_type&latest=30&market_selected=placeholder_type&page=placeholder_page"
# base_url = 'https://www.bangkokassets.com/sellsearch?keyword=&req=full_type&pptid=placeholder_type&p=&c=&l=&ps=0&pe=6,588,750,000&rs=&re=&sarea=&earea=&sland=&eland=&pre=&st=&rec=1&limit=10&page=placeholder_page&order=0&map=0&fix=fixsell'
base_url = "https://api.tb.co.th/api/getPropertyList"

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'TheBestProperty'
get_types = ['LINK','DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d')
date = datetime.today().strftime('%Y-%m-%d')
date_now = fn.get_date_now()


property_type = {
    "home"      : { "type_id": 1, "route": "HOME", "full_type": "BUY", "start": 1, "end": 45 },
    "condo"     : { "type_id": 2, "route": "CONDO", "full_type": "BUY", "start": 1, "end": 22 },
    "townhouse" : { "type_id": 3, "route": "TOWNHOUSE", "full_type": "BUY", "start": 1, "end": 55 },
    "home_rent"      : { "type_id": 1, "route": "HOME", "full_type": "RENT", "start": 1, "end": 2 },
    "condo_rent"     : { "type_id": 2, "route": "CONDO", "full_type": "RENT", "start": 1, "end": 2 },
    "townhouse_rent" : { "type_id": 3, "route": "TOWNHOUSE", "full_type": "RENT", "start": 1, "end": 2 }
}

# ---- Path ----
path_links = os.path.join("links", date, web)
path_files = os.path.join("Files", date, web)

# ---- Create directories if they don't exist ----
os.makedirs(path_links, exist_ok=True)
os.makedirs(path_files, exist_ok=True)


ids = []
webs = []
names = []
house_pictures = []
project_names = []
addresss = []
province_codes = [] #s
district_codes = [] #s
sub_district_codes = [] #s
prices = []
range_of_house_prices = [] #s
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
# ID = 0


def reset_list():
    # เพิ่ม global สำหรับตัวแปรลิสต์ทั้งหมด
    global ids
    global webs
    global names
    global house_pictures
    global project_names
    global addresss
    global province_codes
    global district_codes
    global sub_district_codes
    global prices
    global range_of_house_prices
    global area_SQMs
    global area_SQWs
    global floor_numbers
    global floors
    global sell_type_ids
    global source_ids
    global bedrooms
    global bathrooms
    global garages
    global details
    global latitudes
    global longtitudes
    global duplicates
    global news
    global cross_webs
    global cross_refs
    global days
    global months
    global years
    global post_dates
    global seller_names
    global seller_tels
    global seller_emails
    global seller_ids
    global room_numbers
    global house_links
    global type_ids
    global completion_years
    global date_times

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


def save_link(prop_type):
    print("---------------------::  GET LINK " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    link_type = property_type[prop_type]["full_type"]
    all_data = []  # เก็บข้อมูลทั้งหมดไว้ใน list

    for i in tqdm(range(start_page, end_page)):
        _skip = i * 30
        headers = {
            "Authorization": "api.tb.co.th",
            "Content-Type": "application/json",
            "User-Agent": str(ua.random),
            "Origin": "https://tb.co.th",
            "Referer": "https://tb.co.th/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }

        # ใช้ params แทน data
        params = {
            "tx": [link_type],
            "ipp": 24,
            "market_selected[]": [route],
            "latest": 30,
            "page": i
        }

        # ใช้ requests.get พร้อมกับ params
        req = requests.get(base_url, headers=headers, params=params)
        # print(f"Status Code: {req.status_code}")

        # ตรวจสอบว่า API ตอบกลับสำเร็จหรือไม่
        while req.status_code != 200:
            # print(f"Retrying... Status Code: {req.status_code}")
            req = requests.get(base_url, headers=headers, params=params)

        req.encoding = 'utf-8'
        datas = req.json()

        # ตรวจสอบว่าข้อมูลที่ได้มาถูกต้องและไม่ว่างเปล่า
        if 'propertyList' in datas and 'data' in datas['propertyList']:
            for item in datas['propertyList']['data']:
                if 'property_title' in item and 'id' in item:
                    link = item['property_title']
                    # print()

                    # สร้าง URL ที่ถูกต้อง
                    _link = f"https://tb.co.th/property/{item['property_title']}.p.{item['id']}".replace('ขาย/','ขาย')
                        # .replace(' ','')
                    # print(_link)

                    # บันทึกลงไฟล์
                    with codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8") as file_links:
                        file_links.write(_link + "\n")

                    # รอ 0.3 วินาที
                    sleep(1)
                    file_links.close()


def loop_links(prop_type):
    file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        ids.append(ID)
        link = links[i]
        get_data(link.strip(), type_id, ID)





def get_data(prop_url, type_id, ID ):
    req = requests.get(prop_url)
    req.encoding = "utf-8"
    # req.encoding = "cp874"
    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup)
    # script_tag = soup.find('script', text=lambda t: t and 'window.__NUXT__' in t).get_text().split('locationText')[1]
    # # script_content = script_tag.string
    # print(script_tag)
    # json_text = script_content.split('window.__NUXT__ =', 1)[1].strip().rstrip(';')
    # data = json.loads(script_content)
    # print(data)
    # print(soup)
    try:
        webs.append(web)
        _o = int(0)

        try:
            _names = soup.find('title').get_text()
            # print(_names)
            # _names = data["name"]
            names.append(_names)
        except Exception as err:
            names.append("none")

        try:
            _project_names = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('tag_project:')[1].split('name:')[1].split('}')[0].replace('"','')
            print(_project_names)
            project_names.append(_project_names)
        except Exception as err:
            project_names.append("none")

        try:
            _address = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('locationText')[1].split('spaceTotal')[0].split(',')
            _province_codes = _address[2].replace('"','').replace(':','').replace(' ','')
            _district_codes = _address[1].replace('"','').replace(':','').replace(' ','')
            _sub_district_codes = _address[0].replace('"','').replace(':','').replace(' ','')
            # print(_province_codes,_district_codes,_sub_district_codes)
            _prv, _dis, _subdis = fn.prov_dis_subdis(_province_codes, _district_codes, _sub_district_codes)
            addresss.append(_province_codes + ' ' + _district_codes + ' ' + _sub_district_codes)
            # print(addresss)
            province_codes.append(int(_prv))
            # print(province_codes)
            district_codes.append(int(_dis))
            # print(district_codes)
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

            _prices_sale = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('sale_price')[1]\
            .split('rental_price')[0].replace('.00','').replace('"','').replace(':','').replace(',','')

            _prices_rent = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('rental_price')[1]\
            .split('updated_at')[0].replace('.00','').replace('"','').replace(':','').replace(',','')

            if property_type[prop_type]["full_type"] == "RENT":
                _prices = _prices_rent
            else:
                _prices = _prices_sale
            # print(_pricesx)
            # print(prices)
            prices.append(int(_prices))
            # print(prices)
            range_of_house_prices.append(fn.get_range_of_price(int(_prices)))
            # print(range_of_house_prices)
        except Exception as err:
            prices.append('none')
            range_of_house_prices.append(9)
        #
        try:
            _bedrooms = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('ตัวบ้านมี')[1].split('ห้องนอน')[0].strip()
            bedrooms.append(int(_bedrooms))
            # print(bedrooms)
        except Exception as err:
            bedrooms.append('none')
        #
        try:
            _bathrooms = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('ตัวบ้านมี')[1].split('ห้องน้ำ')[0].split('ห้องนอน')[1].strip()
            # print(_bathrooms)
            # _bathrooms = soup.find('span', {'class': 'cfe8d274', 'aria-label': 'Baths'}).get_text().strip().replace(' ห้องน้ำ', '')
            bathrooms.append(int(_bathrooms))
            # print(bathrooms)
        except Exception as err:
            bathrooms.append('none')
        #
        try:
            area_SQWs_ = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('space_3:')[1].split('area:')[0].replace('"','').replace(',','')
            # area_SQMs_ =soup.find('svg', class_='sc-ejnaz6-14 itMBpO').parent.get_text().replace('ตร.ม.','').strip()
            # .soup.find('svg', class_='sc-ejnaz6-6 iqcoZs')
            area_SQWs_cleaned = re.sub(r'[^0-9.]', '', area_SQWs_)

            # print(area_SQWs_)
            area_SQWs.append(area_SQWs_cleaned)
            # print(area_SQWs)
        except Exception as err:
            area_SQWs.append('none')
        try:
            area_SQMs_ = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('area:')[1].split('property_age')[0].replace('"','').replace('','')
            area_SQMs_cleaned = re.sub(r'[^0-9.]', '', area_SQMs_)

            # print(area_SQMs_cleaned)
            area_SQMs.append(area_SQMs_cleaned)
            # print(area_SQMs)
        except Exception as err:
            area_SQMs.append('none')

        try:
            _detail = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('description:"')[1].split('",href:"')[0].strip()
            # print(_detail)
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _picture = soup.find('meta', property="og:image")
            picture_url = _picture.get('content')
            # print(picture_url)
            # print(_picture)
            # _picture = soup.find('div', class_='sc-aicb4t-0 ieiBqw').find('picture', class_='sc-27ozv5-1 gAHpMv').find('source')['data-src']
            # print(_picture)
            # _picture = data["image"][0]
            house_pictures.append(picture_url)
        except Exception as err:
            house_pictures.append('none')
        #
        try:
            source_ids.append(int(fn.get_source_id(web)))
            # print(source_ids)
        except Exception as err:
            source_ids.append(_o)

        try:
            _floors = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('high_floor:')[1].split(',at_floor')[0].replace('"','')
            _floorss = re.sub(r'[^0-9.]', '', _floors)

            # print(_floorss)
            floors.append(_floorss)
        except Exception as err:
            floors.append("none")

        try:

            _floor_numbers = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text().split('at_floor:')[1].split(',building_name')[0].replace('"','')
            _floor_numberss = re.sub(r'[^0-9.]', '', _floor_numbers)
            # print(_floor_numberss)
            floor_numbers.append(_floor_numberss)
        except Exception as err:
            floor_numbers.append("none")

        # try:
        #     _seller_emails = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())['props']['pageProps'][
        #         'adDetail']['ad']['member']["email"]
        #     # _seller_tels1 =_seller_tels["telephone"]
        #     # print(_seller_emails)
        #     # _seller_tels = data["offers"][0]["offeredBy"]["telephone"]
        #     seller_emails.append(_seller_emails)
        # except Exception as err:
        #     seller_emails.append("none")

        try:
            _map = soup.find('script', text=lambda text: text and 'window.__NUXT__' in text).get_text()
            # .split('lat:"')[1].split('",lng:')[0]
            # ['adDetail']\
            #                ['ad']['locations'][0]
            # print(_map)
            _latitudes = _map.split('lat:"')[1].split('",lng:')[0]
            # print(_latitudes)
            _longtitudes = _map.split('lng:"')[1].split('",high_floor:')[0]
            # print(_longtitudes)

            # _longtitudes = _map['lng']
            # # print(_latitudes,_longtitudes)
            latitudes.append(_latitudes)
            longtitudes.append(_longtitudes)

        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')

        try:
            if property_type[prop_type]["full_type"] == "RENT":
                _sell_type_ids = int(2)
            else:
                _sell_type_ids = int(1)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))

        # floor_numbers.append('none')
        # floors.append('none')
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
        seller_names.append('none')
        seller_tels.append('none')
        seller_emails.append('none')
        cross_webs.append('none')
        cross_refs.append('none')
        house_links.append(prop_url)
        type_ids.append(type_id)
        date_times.append(date_now)

        # print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)


if __name__ == '__main__':

    for get_type in get_types:
        if get_type == 'LINK':
            for prop_type in property_type:
                save_link(prop_type)
                # break

        if get_type == "DATA":
            _start_date = datetime.now()
            for prop_type in property_type:
                print("---------------------::  GET DATA " + prop_type + "  ::---------------------")
                # เรียกใช้ฟังก์ชัน reset_list() ที่แก้ไขแล้ว
                reset_list()
                loop_links(prop_type)

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

                property_list.to_csv(path_files + '/' + web + "_" + prop_type + '.csv')
                print('Export', len(ids), 'Rows To CSV File Completed!!!! ')
                print('Start At ', _start_date)
                print('Success At ', datetime.now())

                # ไม่ต้องเรียก reset_list() ซ้ำตรงนี้แล้ว
                property_list = None

                # break
                
            # check data
            fn.check_data(date, web)

            # send line message on success.
            fn.send_message(date, web)

            # upload files to google drive.
            fn.upload_processing(date, web)
