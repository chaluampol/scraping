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

import reic_function as fn
from fake_useragent import UserAgent

# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

web = "baania"
base_url = 'https://www.baania.com/th/s/%E0%B8%97%E0%B8%B1%E0%B9%89%E0%B8%87%E0%B8%AB%E0%B8%A1%E0%B8%94/listing?mapMove=true&page=placeholder_page&propertyType=placeholder_type&sellState=placeholder_property_sell_rent,sale-rent&sort.created=desc'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
        "home"          : {"type_id": 1, "route": "1", "property_sell_rent": 'on-sale', "start": 1, "end": 12},
        "condo"         : {"type_id": 2, "route": "2", "property_sell_rent": 'on-sale', "start": 1, "end": 7},
        "townhouse"     : {"type_id": 3, "route": "3", "property_sell_rent": 'on-sale', "start": 1, "end": 10},
        "home_rent"     : {"type_id": 1, "route": "1", "property_sell_rent": 'on-rent', "start": 1, "end": 2},
        "condo_rent"    : {"type_id": 2, "route": "2", "property_sell_rent": 'on-rent', "start": 1, "end": 2},
        "townhouse_rent": {"type_id": 3, "route": "3", "property_sell_rent": 'on-rent', "start": 1, "end": 2}
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


def get_data(prop_url, type_id, ID):
    # print(prop_url)

    Headers = {'User-Agent': ua.random}
    req = requests.get(prop_url, headers=Headers)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')
    _o = int(0)
    sleep(0.3)

    try:
        _data = str(soup.find('script', id='__NEXT_DATA__')).replace(
            '<script id="__NEXT_DATA__" type="application/json">',
            '').replace('</script>', '')
        _data_json = json.loads(_data)
        _prop_data = _data_json['props']['pageProps']['listing']['data']
        # print(_prop_data)
        _prop_project = _prop_data['project']

        # ID += 1
        ids.append(ID)
        webs.append(web)

        try:
            _prop_address = _prop_data['address']
            _province = _prop_address['province_th']
            _district = _prop_address['district_th']
            _sub_district = _prop_address['subdistrict_th']
            addresss.append(_sub_district + ' ' + _district + ' ' + _province)
        except Exception as err:
            _province = 'none'
            _district = 'none'
            _sub_district = 'none'
            addresss.append('none')

        try:
            _prv_code, _dis_code, subdis_code = fn.prov_dis_subdis(_province, _district, _sub_district)
            province_codes.append(int(_prv_code))
            district_codes.append(int(_dis_code))
            sub_district_codes.append(int(subdis_code))
        except Exception as err:
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')


        try:
            name = soup.find('title').get_text().strip().replace('\n', '').replace('\t', '')
            names.append(name)
        except Exception as err:
            names.append('none')

        try:
            project_names.append(_prop_project['title'])
        except Exception as err:
            project_names.append('none')

        try:
            if property_type[prop_type]["property_sell_rent"] == "on-sale":
                _price = _prop_data['financial']['price_listing']
            else:
                _price = _prop_data['financial']['price_renting']
            prices.append(int(_price))
            range_of_house_prices.append(int(fn.get_range_of_price(_price)))
        except Exception as err:
            prices.append(_o)
            range_of_house_prices.append(9)


        try:
            _SQM = _prop_data['detail']['area_usable']
            if _SQM == None:
                _SQM = 0
            area_SQMs.append(_SQM)
        except Exception as err:
            area_SQMs.append(0)

        try:
            _rai = _prop_data['detail']['area_land']['rai']
            if _rai == None:
                _rai = 0
            _ngan = _prop_data['detail']['area_land']['ngan']
            if _ngan == None:
                _ngan = 0
            _wa = _prop_data['detail']['area_land']['wa']
            if _wa == None:
                _wa = 0

            _SQW = str(float(_rai) * 1600 + float(_ngan) * 400 + float(_wa) * 4)
            area_SQWs.append(_SQW)
        except Exception as err:
            area_SQWs.append(0)

        try:
            seller_tels.append(str(_prop_data['contact_info']).replace('-', ''))
        except Exception as err:
            seller_tels.append('none')

        try:
            seller_names.append(_prop_data['contact']['contact_name'])
        except Exception as err:
            seller_names.append('none')

        try:
            seller_emails.append(_prop_data['contact']['contact_email'])
        except Exception as err:
            seller_emails.append('none')

        try:
            if property_type[prop_type]["property_sell_rent"] == "on-sale":
                _sell_type_ids = int(1)
            else:
                _sell_type_ids = int(2)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))


        try:
            room_numbers.append(int(_prop_data['detail']['num_room']))
        except Exception as err:
            room_numbers.append('none')

        try:
            bedrooms.append(int(_prop_data['detail']['num_bed']))
        except Exception as err:
            bedrooms.append('none')

        try:
            bathrooms.append(int(_prop_data['detail']['num_bath']))
        except Exception as err:
            bathrooms.append('none')

        try:
            garages.append(int(_prop_data['detail']['num_parking']))
        except Exception as err:
            garages.append('none')

        try:
            _detail = str(_prop_data['general']['detail']).replace('\r', '').replace('<br>', '').replace('<p>', '').replace('</p>', ' ').replace('&nbsp;', ' ').replace('  ', ' ')
            _soup = BeautifulSoup(_detail, 'html.parser')
            details.append(_soup.get_text().replace('\r', '').replace('<br>', '').replace('<p>', '').replace('</p>', ' ').replace('&nbsp;', ' ').replace('  ', ' ').replace('\n', ''))
        except Exception as err:
            details.append('none')

        try:
            latitudes.append(_prop_data['location']['lat'])
        except Exception as err:
            latitudes.append('none')

        try:
            longtitudes.append(_prop_data['location']['lon'])
        except Exception as err:
            longtitudes.append('none')

        duplicates.append(_o)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')

        try:
            num_floors = _prop_data['detail']['num_floor']
            if type_id == 1 or type_id == 3:
                floors.append('none')
                floor_numbers.append(num_floors)
            else:
                floors.append(num_floors)
                floor_numbers.append('none')
        except:
            floor_numbers.append('none')
            floors.append('none')


        try:
            house_pictures.append(_prop_data['images']['main']['url'])
        except Exception as err:
            house_pictures.append('none')

        try:
            source_ids.append(int(fn.get_source_id(web)))
        except Exception as err:
            source_ids.append(_o)

        house_links.append(prop_url)
        type_ids.append(int(type_id))

        # รอวิจัยบอกว่าได้ใช้งานหรือไม่
        seller_ids.append(_o)
        completion_years.append('none')

        try:
            _post_date = str(_data_json['props']['pageProps']['listing']['timeFormated']['updated_at']).split('/')
            _day = _post_date[0]
            _month = _post_date[1]
            _year = _post_date[2]
            days.append(int(_day))
            months.append(int(_month))
            years.append(int(_year))
            post_dates.append(_year + '-' + _month + '-' + _day)
        except Exception as err:
            days.append('none')
            months.append('none')
            years.append('none')
            post_dates.append('none')

        date_times.append(date_now)

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
        get_data(link.strip().replace('\ufeff', ''), type_id, ID)
        # break


def save_list_links(prop_type):
    print("---------------------::  " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type]["property_sell_rent"]
    req_url = base_url.replace("placeholder_type", route).replace("placeholder_property_sell_rent", str(list_type))

    for i in tqdm(range(start_page, end_page)):
        wait_time = 0.5
        url = req_url.replace("placeholder_page", str(i))
        # print(url)
        Headers = {'User-Agent': ua.random}
        req = requests.get(url, headers=Headers)
        while req.status_code != 200:
            req = requests.get(url, headers=Headers)

        soup = BeautifulSoup(req.text, 'html.parser')
        _listing = soup.find_all('div', class_='mb-3 col')

        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for j in _listing:
            _link = 'https://www.baania.com' + j.find('a')['href']
            file_links.writelines(_link + "\n")
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

            # send line message on success.
            fn.send_message(date, web)
