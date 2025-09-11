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
from urllib.parse import quote  # ใช้เข้ารหัสพวกชื่อ property

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()



# base_url = 'https://homehug.in.th/search?search=1&lat=15.90568418&lng=101.45705990&zoom=6&listingType=placeholder_sale_rent' \
#            '&propertyType=placeholder_type&beds=0,1,2,3,4,5,6&baths=0,1,2,3,4,5,6'
# base_url = 'https://www.homehug.in.th/search?search=1&zoom=11&statusZoom=1&statusSearch=0&listingType=placeholder_sale_rent&propertyType=placeholder_type&beds=&baths=&minPrice=&maxPrice=&text='

# property_type = {
#     "home"          : {"type_id": 1, "route": "1", "property_sell_rent": 1, "start": 1, "end": 182},
#     "condo"         : {"type_id": 2, "route": "2", "property_sell_rent": 1, "start": 1, "end": 124},
#     "townhouse"     : {"type_id": 3, "route": "3", "property_sell_rent": 1, "start": 1, "end": 172},
#     "home_rent"     : {"type_id": 1, "route": "1", "property_sell_rent": 1, "start": 1, "end": 53},
#     "condo_rent"    : {"type_id": 2, "route": "2", "property_sell_rent": 1, "start": 1, "end": 70},
#     "townhouse_rent": {"type_id": 3, "route": "3", "property_sell_rent": 1, "start": 1, "end": 35},
# }

# base_url = 'https://www.homehug.in.th/placeholder_sale_rent-placeholder_type?beds=&baths=&minPrice=&maxPrice=&searchword='


# base_url = 'https://apicore.home.co.th/api/keywordpattern/placeholder_sale_rent-placeholder_type?pageSize=12&page=2&sort=6&useWeb=homehug&beds=&baths=&minPrice=&maxPrice=&searchword='
base_url = 'https://apicore.home.co.th/api/keywordpattern/{sell_rent}-{prop_type}'

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'homemarket'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
    "home":          {"type_id": 1, "route": "บ้าน",        "property_sell_rent": "ขาย", "start": 1, "end": 590},
    "condo":         {"type_id": 2, "route": "คอนโด",       "property_sell_rent": "ขาย", "start": 1, "end": 168},
    "townhouse":     {"type_id": 3, "route": "ทาวน์โฮม",    "property_sell_rent": "ขาย", "start": 1, "end": 275},
    "home_rent":     {"type_id": 1, "route": "บ้าน",        "property_sell_rent": "เช่า", "start": 1, "end": 137},
    "condo_rent":    {"type_id": 2, "route": "คอนโด",       "property_sell_rent": "เช่า", "start": 1, "end": 59},
    "townhouse_rent":{"type_id": 3, "route": "ทาวน์โฮม",    "property_sell_rent": "เช่า", "start": 1, "end": 48},
}

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

            try:
                location_tag = soup.find('div', class_='flex pt-2')
                if location_tag:
                    _location_detail = location_tag.get_text().replace('ที่ตั้ง', '')
                    parts = _location_detail.split()

                    if len(parts) >= 3:
                        _sub_district = parts[-3]
                        _district = parts[-2]
                        _province = parts[-1]
                        _prv_code, _dis_code, _subdis_code = fn.prov_dis_subdis(_province, _district, _sub_district)
                        province_codes.append(_prv_code)
                        district_codes.append(_dis_code)
                        sub_district_codes.append(_subdis_code)
                        addresss.append(_sub_district + ' ' + _district + ' ' + _province)
                        # print(_sub_district)
                    else:
                        raise ValueError("Not enough location parts")
                else:
                    raise ValueError("Location tag not found")
            except Exception as err:
                province_codes.append('none')
                district_codes.append('none')
                sub_district_codes.append('none')
                addresss.append('none')

            try:
                _price = soup.find('p', class_='text-[22px] font-semibold mt-1').get_text().replace('฿', '').replace(',', '').strip()
                # print(_price)
                # _price = int(re.sub('[^0-9]', '', soup.find('span', class_='mb-0 title-price').get_text().strip()))
                prices.append(_price)
                range_of_house_prices.append(fn.get_range_of_price(_price))
            except Exception as err:
                prices.append(0)
                range_of_house_prices.append(0)

            try:
                detail_text = soup.find('div', class_='flex items-center space-x-6 text-gray-600 mt-6').get_text()
                # print(detail_text)
                match = re.search(r'([\d.]+)\s*ตร\.ว', detail_text)
                if match:
                    area_SQWs.append(match.group(1))
                else:
                    area_SQWs.append('none')
                # print(area_SQWs)
                # area_SQMs.append(
                #     soup.find('div', class_='card-section1').find('p', class_='title-spec').get_text().strip())
            except Exception as err:
                area_SQWs.append('none')

            try:
                detail_text = soup.find('div', class_='flex items-center space-x-6 text-gray-600 mt-6').get_text()
                # print(detail_text)
                match = re.search(r'([\d.]+)\s*ตร.ม', detail_text)
                if match:
                    area_SQMs.append(match.group(1))
                else:
                    area_SQMs.append('none')
                # print(area_SQMs)

            except Exception as err:
                area_SQMs.append('none')

            # area_SQWs.append('none')
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
                detail_text = soup.find('div', class_='flex items-center space-x-6 text-gray-600 mt-6').get_text()
                match = re.search(r'(\d+)\s*นอน', detail_text)
                if match:
                    bedrooms.append(match.group(1))
                else:
                    bedrooms.append('none')
                # print(bedrooms)
            except Exception as err:
                bedrooms.append('none')
            try:
                bathroomss = soup.find('div', class_='flex items-center space-x-6 text-gray-600 mt-6').get_text()
                match = re.search(r'(\d+)\s*น้ำ', bathroomss)
                if match:
                    bathrooms.append(match.group(1))
                else:
                    bathrooms.append('none')
                # print(bedrooms)
            except Exception as err:
                bathrooms.append('none')

            garages.append('none')

            try:
                _detail = soup.find('div', class_='whitespace-pre-line').get_text().replace('\n', '').replace('\r','').replace(',', ' ')
                # print(_detail)
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

                img = soup.find('img', class_='transition-all duration-300 object-cover rounded-l-2xl w-full h-full bg-[#EAE8DF]')['src']
                _house_picturess ='https://www.homehug.in.th'+ img
                # find('img', class_='lazy')['data-src']
                # print(_house_picturess)
                if _house_picturess == '':
                    _house_picturess = 'none'
                house_pictures.append(_house_picturess if _house_picturess else 'none')
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

            # print('Get Data OK')
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
        sleep(0.2)
        # break



def save_list_links(prop_type):
    print("---------------------::  GET LINK " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = quote(property_type[prop_type]["route"])
    link_type = quote(property_type[prop_type]["property_sell_rent"])

    for i in tqdm(range(start_page, end_page)):
        url = base_url.format(sell_rent=link_type, prop_type=route)

        params = {
            "pageSize": 12,
            "page": i,
            "sort": 6,
            "useWeb": "homehug",
            "beds": "",
            "baths": "",
            "minPrice": "",
            "maxPrice": "",
            "searchword": ""
        }

        headers = {
            "Authorization": "ZWQ3ZTk4MTlmZmJmNDI5YzliOWJiNDU3NmM5NzFhYTZhNmVkMjI1Yw==",
            "Content-Type": "application/json",
            "User-Agent": str(ua.random),
            "Host": "apicore.home.co.th",
            "Origin": "https://www.homehug.in.th",
            "Referer": "https://www.homehug.in.th/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site"
        }

        req = requests.get(url, headers=headers, params=params)
        _data = json.loads(req.text)
        # print(_data)


        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for i in _data['DataResult']['Listing']['dataList']:
            # print(i)
            _link = 'https://market.home.co.th/realestate/' + i['title'].replace(' ', '-').replace('\n', '') + '-' + str(i['listingID'])
            # print(_link)
            file_links.writelines(_link + "\n")
        file_links.close()
        sleep(0.3)

if __name__ == '__main__':

    for get_type in get_types:
        if get_type == 'LINK':
            for prop_type in property_type:
                save_list_links(prop_type)
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

