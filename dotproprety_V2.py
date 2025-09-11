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
import ssl
import cloudscraper
import reic_function as fn
from fake_useragent import UserAgent

# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()


# base_url = "https://www.dotproperty.co.th/placeholder_type?sort=newest&page=placeholder_page%22"
base_url = "https://www.dotproperty.co.th/placeholder_type?page=placeholder_page&sortBy=verification_at%7Cdesc"
# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'dotproprety'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
    "home_sale"        : {"type_id": 1, "route": "houses-for-sale", "start": 1, "end": 20},
    "condo_sale"       : {"type_id": 2, "route": "condos-for-sale", "start": 1, "end": 20},
    "townhouse_sale"   : {"type_id": 3, "route": "townhouses-for-sale", "start": 1, "end": 20},
    "home_rent"        : {"type_id": 1, "route": "houses-for-rent", "start": 1, "end": 20},
    "condo_rent"       : {"type_id": 2, "route": "condos-for-rent", "start": 1, "end": 20},
    "townhouse_rent"   : {"type_id": 3, "route": "townhouses-for-rent", "start": 1, "end": 20}
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


rand = randint(1000, 10000)
browsers = ['chrome', 'firefox']
platforms = [
                {'platform': 'linux', 'mobile': False, 'desktop': True},
                {'platform': 'windows', 'mobile': False, 'desktop': True},
                {'platform': 'darwin', 'mobile': False, 'desktop': True},
                {'platform': 'android', 'mobile': True, 'desktop': False}
            ]

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

def get_data(prop_url, type_id, ID):
    # print(prop_url)

    Headers = {'User-Agent': ua.random}
    req = requests.get(prop_url, headers=Headers)
    # print(req.status_code)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')

    try:
        webs.append(web)
        ids.append(ID)
        house_links.append(prop_url)
        type_ids.append(int(type_id))
        _o = int(0)

        try:
            name = soup.find('title').get_text().replace(',', '')
            # print(name)
            names.append(name)
        except Exception as err:
            names.append('none')

        try:
            _project_names = soup.find('div', class_='user-company-detail').find('div', class_='heading').get_text().strip().replace('เกี่ยวกับ ', '').replace('Details on ', '').replace(',', '')
            project_names.append(_project_names)
        except Exception as err:
            project_names.append('none')

        try:
            _address = soup.find('div', class_='text-lg font-normal').get_text().strip().replace(' ', '').split(',')
            # print(_address)

            if len(_address) < 3:
                _address.append('none')
            _prv, _dis, _subdis = fn.prov_dis_subdis(_address[2], _address[1], _address[0])
            # print(_prv)

            if _address[2] == 'none':
                addresss.append(_address[1] + ' ' + _address[0])
            else:
                addresss.append(_address[2] + ' ' + _address[1] + ' ' + _address[0])
            province_codes.append(int(_prv))
            district_codes.append(int(_dis))
            sub_district_codes.append(_subdis)
        except:
            addresss.append('none')
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')


        try:
            _price = soup.find('div', class_='group relative flex flex-col gap-2 sm:flex-row').get_text().strip().replace(',', '').replace('฿', '').replace('\n', '').replace('\r', '')
            # print(_price)
            prices.append(_price)
            range_of_house_prices.append(int(fn.get_range_of_price(_price)))
        except Exception as err:
            prices.append(_o)
            range_of_house_prices.append(9)
        #
        try:
            _bedrooms = soup.find('div', class_='flex w-full flex-col items-center justify-center text-center sm:flex-row').parent.parent.get_text().split('ห้องนอน')[0]
            # print(_bedrooms)
            bedrooms.append(int(_bedrooms))


        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms =soup.find('div', class_='flex w-full flex-col items-center justify-center text-center sm:flex-row').parent.parent.get_text().split('ห้องนอน')[1].split('ห้องน้ำ')[0]
            # print(_bathrooms)
            bathrooms.append(int(_bathrooms))
        except Exception as err:
            bathrooms.append('none')

        try:
            _areaW = soup.find('div', class_='flex w-full flex-col items-center justify-center text-center sm:flex-row').parent.parent.get_text().split('ตรม.')[1]
            # print(_areaW)
            if type_id == 1 or type_id == 3:
                area_SQWs.append(_areaW)
            else:
                area_SQWs.append('none')
        except Exception as err:
            area_SQWs.append('none')


        try:
            _areaM = soup.find('div', class_='flex w-full flex-col items-center justify-center text-center sm:flex-row').parent.parent.get_text().split('ตรม.')[0].split('ห้องน้ำ')[1]
            # print(_areaM)
            area_SQMs.append(_areaM)
        except Exception as err:
            area_SQMs.append('none')

        try:
            _details = soup.find('p', class_='text-base font-light text-gray-700 [&_a]:text-accent').get_text().strip().replace(',', ' ').replace('\n', ' ').replace('\r', ' ')
            # print(_details)
            details.append(_details)

        except Exception as err:
            details.append('none')

        try:
            num_floors = soup.find('div',class_='grid w-full grid-cols-2 gap-6 xl:grid-cols-3').get_text().split('ชั้น')[1].split('ห้อง')[0].replace('สตูดิโอสตูดิโอ','')
            # print(num_floors)
                # .parent.text.replace('จำนวนชั้น', '')
            if type_id == 1 or type_id == 3:
                floors.append('none')
                floor_numbers.append(num_floors)
            else:
                floors.append(num_floors)
                floor_numbers.append('none')
        except Exception as err:
            floors.append('none')
            floor_numbers.append('none')


        try:
            _picture = soup.find('ul', class_='gallery-list with-enquiry-form').find('li')['data-exthumbimage']
            house_pictures.append(_picture)
        except Exception as err:
            house_pictures.append('none')

        try:
            source_ids.append(int(fn.get_source_id(web)))
        except Exception as err:
            source_ids.append(_o)

        try:
            _seller_names = soup.find('div', class_='agent-company-name').get_text().strip()
            seller_names.append(_seller_names)
        except Exception as err:
            seller_names.append('none')

        try:
            list_types = property_type[prop_type]["route"].replace("houses-for-", "").replace("condos-for-", "").replace("townhouses-for-", "")
            if list_types == "sale":
                _sell_type_ids = int(1)
            else:
                _sell_type_ids = int(2)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))


        seller_ids.append(_o)
        seller_tels.append('none')
        seller_emails.append('none')
        days.append('none')
        months.append('none')
        years.append('none')
        post_dates.append('none')
        date_times.append(date_now)
        garages.append('none')
        room_numbers.append('none')
        duplicates.append(_o)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        latitudes.append('none')
        longtitudes.append('none')
        completion_years.append('none')


        # print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)



def loop_links(prop_type):
    file_links = codecs.open(path_links + f'/links_{prop_type}.txt', 'r', 'utf-8')
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    ID = 0
    for j in tqdm(range(len(links))):
        ID += 1
        # ids.append(ID)
        link = links[j]
        get_data(link.strip(), type_id, ID)




def save_list_links(prop_type):
    print("---------------------::  " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    req_url = base_url.replace("placeholder_type", route)

    for i in tqdm(range(start_page, end_page)):
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        # print(url)
        Headers = {'User-Agent': ua.random}
        req = scraper.get(url, headers=Headers)


        # print(req.status_code)
        while req.status_code != 200:
            req = requests.get(url, headers=Headers)
        #
        soup = BeautifulSoup(req.text, 'html.parser')
        # print(soup)
        _content = soup.find_all('a', class_='no-title relative')
        # print(_content)

        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for j in _content:
            _link = j['href']
            # print(_link)
            file_links.writelines("https://www.dotproperty.co.th/"+_link + "\n")
        file_links.close()
        sleep(wait_time)
        # break


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
