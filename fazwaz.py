import sys
import os
import requests
import codecs
import re
import json
import pyautogui
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

base_url = 'https://www.fazwaz.co.th/placeholder_property_sell_rent?type=placeholder_type&order_by=created_at|desc&mapEnable=0&page=placeholder_page'

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'fazwaz'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
        "home"          : {"type_id": 1, "route": "house",     "property_sell_rent": 'ขายบ้าน', "start": 1, "end": 37},
        "condo"         : {"type_id": 2, "route": "condo",     "property_sell_rent": 'ขายบ้าน', "start": 1, "end": 52},
        "townhouse"     : {"type_id": 3, "route": "townhouse", "property_sell_rent": 'ขายบ้าน', "start": 1, "end": 7},
        "home_rent"     : {"type_id": 1, "route": "house",     "property_sell_rent": 'บ้านให้เช่า', "start": 1, "end": 25},
        "condo_rent"    : {"type_id": 2, "route": "condo",     "property_sell_rent": 'บ้านให้เช่า', "start": 1, "end": 65},
        "townhouse_rent": {"type_id": 3, "route": "townhouse", "property_sell_rent": 'บ้านให้เช่า', "start": 1, "end": 7}
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


def get_data(prop_url, type_id, ID):
    Headers = {'User-Agent': ua.random}
    req = requests.get(prop_url, headers=Headers)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')

    try:
        try:
            name = soup.find('title').get_text().split('|')[0].strip().replace(',', '')
            names.append(name)
        except Exception as err:
            names.append('none')

        try:
            _project_names = soup.find(text='ชื่อโครงการ:').parent.find_next_siblings('a')[0].get_text().strip().replace(",", "")
            project_names.append(_project_names)
        except Exception as err:
            project_names.append('none')

        try:
            _addresss = soup.find('div', class_='clear_flex').find('span', class_='project-location').get_text().strip().replace(' ', '').split(',')
            _prv_code, _dis_code, _subdis_code = fn.prov_dis_subdis(_addresss[2], _addresss[1], _addresss[0])

            addresss.append(_addresss)
            province_codes.append(int(_prv_code))
            district_codes.append(int(_dis_code))
            sub_district_codes.append(int(_subdis_code))
        except Exception as err:
            addresss.append(0)
            province_codes.append(0)
            district_codes.append(0)
            sub_district_codes.append(0)


        try:
            sell_rent = property_type[prop_type]["property_sell_rent"]
            if sell_rent == 'ขายบ้าน':
                _price = int(re.sub('[^0-9]', '', soup.find('div', class_='gallery-unit-sale-price__price').get_text().strip()))
            elif sell_rent == 'บ้านให้เช่า':
                _price = int(re.sub('[^0-9]', '', soup.find('div', class_='gallery-unit-rent-price__price').get_text().strip()))

            prices.append(_price)
            range_of_house_prices.append(fn.get_range_of_price(_price))
        except Exception as err:
            prices.append(0)
            range_of_house_prices.append(9)

        try:
            sell_rent = property_type[prop_type]["property_sell_rent"]
            if sell_rent == 'ขายบ้าน':
                _sell_type_ids = 1
            elif sell_rent == 'บ้านให้เช่า':
                _sell_type_ids = 2
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(4)

        try:
            _area_SQMs = soup.find(text="พื้นที่ใช้สอย").parent.parent.get_text().strip().split('\n')[0].split(' ')[0]
            area_SQMs.append(_area_SQMs)
        except Exception as err:
            area_SQMs.append('none')


        try:
            _area_SQWs = soup.find(text="ขนาดที่ดิน").parent.parent.get_text().strip().split('\n')[1].split(' ')[0]
            area_SQWs.append(_area_SQWs)
        except Exception as err:
            area_SQWs.append('none')

        try:
            _bedrooms = soup.find(text=" ห้องนอน").parent.parent.get_text().strip().strip(' ')[0]
            bedrooms.append(_bedrooms)
        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms = int(re.sub('[^0-9]', '',  soup.find('div', class_='header-detail-page__right')
                                    .find_all('div', class_='property-info-element')[1].get_text().strip()))
            bathrooms.append(_bathrooms)
        except Exception as err:
            bathrooms.append('none')

        try:
            _garages = int(re.sub('[^0-9]', '', soup.find(text="ที่จอดรถ (คัน)").parent.parent.get_text().strip()))
            garages.append(_garages)
        except Exception as err:
            garages.append('none')

        try:
            _completion_years = soup.find('div', class_='header-detail-page__right').find_all('div', class_='property-info-element')[4].get_text().strip().split('\n')
            if _completion_years[1] == 'สร้างเสร็จแล้ว':
                _completion_yearss = _completion_years[0].split(' ')[1]
            else:
                _completion_yearss = 'none'
            completion_years.append(_completion_yearss)
        except Exception as err:
            completion_years.append('none')

        try:
            if type_id == 1 or type_id == 3:
                _num_floors = soup.find(text="จำนวนชั้น").parent.parent.get_text().strip().split('\n')[1]
                floors.append('none')
                floor_numbers.append(_num_floors)
            else:
                _num_floors = soup.find(text="ชั้น").parent.parent.get_text().strip().split('\n')[1]
                floors.append(_num_floors)
                floor_numbers.append('none')
        except Exception as err:
            floors.append('none')
            floor_numbers.append('none')


        try:
            _detail = soup.find('div', {'class': 'unit-view-description'}).get_text().strip().replace('อสังหาริมทรัพย์นี้เป็น', '')\
                .replace('\n', ' ').replace('\r', '').replace(',', '')
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _house_pictures = soup.find('a', {'class': 'photo-gallery-detail-page__main-box'}).img['src']
            house_pictures.append(_house_pictures)
        except Exception as err:
            house_pictures.append('none')

        try:
            _post_date = soup.find('div', {'class': 'basic-information'}).find(text='ลงประกาศเมื่อ').parent.parent.get_text().strip()\
                .replace('ลงประกาศเมื่อ', '').replace('\n', '').replace('\r', '').replace(',', '').split(' ')
            _day = _post_date[0]
            _month = thai_abbr_months.index(str(_post_date[1])) + 1
            _year = int(_post_date[2]) - 543
            days.append(_day)
            months.append(_month)
            years.append(_year)
            post_dates.append(str(_year) + '-' + str(_month) + '-' + str(_day))
        except Exception as err:
            days.append('none')
            months.append('none')
            years.append('none')
            post_dates.append('none')


        ids.append(ID)
        webs.append(web)
        date_times.append(date_now)
        room_numbers.append('none')
        source_ids.append(fn.get_source_id(web))
        seller_names.append('none')
        seller_tels.append('none')
        seller_emails.append('none')
        # seller_id ยังไม่ได้ทำ รอคำตอบจาก RS ว่าได้ใช้งานหรือไม่
        seller_ids.append(0)
        latitudes.append('none')
        longtitudes.append('none')
        duplicates.append(0)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        house_links.append(prop_url)
        type_ids.append(int(type_id))


        # print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)


def loop_links(prop_type):
    file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    # sell_rent = property_type[prop_type]['property_sell_rent']
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        link = links[i]
        get_data(link.strip(), type_id, ID)
        # break
        sleep(0.5)



def save_list_links(prop_type):
    print("---------------------::  " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type]["property_sell_rent"]
    req_url = base_url.replace("placeholder_type", route).replace("placeholder_property_sell_rent", str(list_type))

    for i in tqdm(range(start_page, end_page)):
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        # print(url)
        Headers = {'User-Agent': ua.random}
        req = requests.get(url, headers=Headers)
        while req.status_code != 200:
            req = requests.get(url, headers=Headers)

        soup = BeautifulSoup(req.text, 'html.parser')
        _listing = soup.find('div', class_='result-search__row units_loading_wrapper').find_all('div', class_='loaded')
        # print(_listing)
        link_elements = []  # Create an empty list to store the link elements

        for i in _listing:
            link_elements.extend(
                i.find_all('a', class_='link-unit'))  # Extend the list with elements from each iteration
            # print(link_elements)  # Optional: print the link elements for debugging

        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for j in link_elements:
            _link = j['href']  # Use square brackets to access the 'href' attribute
            # print(_link)
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
                
            # check data
            fn.check_data(date, web)

            # send line message on success.
            fn.send_message(date, web)

            # upload files to google drive.
            fn.upload_processing(date, web)