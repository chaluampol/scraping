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
import pyautogui
import pyperclip
import cloudscraper
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint, randrange
from datetime import datetime, timedelta
from random import randint
from fake_useragent import UserAgent
import  json

ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

base_url = 'https://propertyscout.co.th/r_type/placeholder_type/ล่าสุด/หน้า-placeholder_page/'

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'propertyscout'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
    "home"      : { "type_id": 1, "route": "บ้านเดี่ยว", "r_type": "ขาย", "start": 49, "end": 60},
    "condo"     : { "type_id": 2, "route": "คอนโด", "r_type": "ขาย", "start": 2, "end": 60},
    "townhouse" : { "type_id": 3, "route": "ทาวน์เฮ้าส์", "r_type": "ขาย", "start": 2, "end": 25},
    "home_rent"      : { "type_id": 1, "route": "บ้านเดี่ยว", "r_type": "ให้เช่า", "start": 2, "end": 25},
    "condo_rent"     : { "type_id": 2, "route": "คอนโด", "r_type": "ให้เช่า", "start": 54, "end": 60},
    "townhouse_rent" : { "type_id": 3, "route": "ทาวน์เฮ้าส์", "r_type": "ให้เช่า", "start": 17, "end": 25}
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
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type]["r_type"]
    req_url = base_url.replace("placeholder_type", str(route)).replace("r_type", str(list_type))

    for i in tqdm(range(start_page, end_page)):
        wait_time = 0.5
        url = req_url.replace("placeholder_page", str(i))
        req = requests.get(url)
        # print(req.status_code)
        soup = BeautifulSoup(req.text, 'html.parser')

        # list = soup.find("div", {"id": "listing-card-container"}).find_all("a", {"class": "w-full"})

        list = json.loads(soup.find_all('script', {'type': 'application/ld+json'})[1].text)
        liks= list["offers"]['offers']
        file_links = codecs.open(path_links + f"/link_{prop_type}.txt", "a+", "utf-8")
        for j in liks:
        #     # print(j)
            _link = j["url"]
            # print(_link)
            file_links.writelines(_link+ "\n")
        file_links.close()
        sleep(wait_time)


def loop_links(prop_type):
    file_links = codecs.open(path_links + f"/link_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]["type_id"]
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        link = links[i]
        get_data(link.strip(), type_id, ID)
        file_links.close
        sleep(0.5)


def get_data(prop_url, type_id, ID ):
    req = requests.get(prop_url)
    req.encoding = "utf-8"
    # req.encoding = "cp874"
    soup = BeautifulSoup(req.text, 'html.parser')
    try:
        ids.append(ID)
        webs.append(web)
        post_dates.append(date)
        house_links.append(prop_url)
        type_ids.append(type_id)
        garages.append('none')
        duplicates.append(0)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        room_numbers.append('none')
        seller_ids.append(0)
        date_times.append(date_now)
        completion_years.append('none')
        days.append('none')
        months.append('none')
        years.append('none')
        project_names.append('none')
        seller_names.append('none')
        seller_emails.append('none')
        seller_tels.append('none')
        area_SQWs.append('none')
        floor_numbers.append('none')
        # details.append('none')

        try:
            _names = soup.find('section', class_='mb-8 max-md:mb-8').find('h1', class_='leading-snug text-3xl md:text-4xl font-bold mb-3').get_text().strip()
            # print(_names)
            names.append(_names)

        except Exception as err:
            names.append('none')

        try:
            _house_pictures = soup.find('div', class_='cursor-pointer rounded-md relative overflow-hidden min-h-collage-main rounded-none').img['src']
            # print(_house_pictures)
            # _link_house_pictures = "https://www.bangkokassets.com"+_house_pictures
            # print(_link_house_pictures)
            house_pictures.append(_house_pictures)

        except Exception as err:
            house_pictures.append('none')

        # try:
        #     _project_name = _project_names = soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split()[4]
        #     if _project_name == 'ไม่มีข้อมูล':
        #         _project_name = 'none'
        #     project_names.append(_project_name)
        # except Exception as error:
        #     project_names.append('none')

        try:
            _addresss =soup.find('section', class_='mb-8 max-md:mb-8').find('p', class_='text-lg flex items-center').get_text().strip().replace(',','')

            _locationss = _addresss.split()
            _province_codes = _locationss[3]
            _district_codes = _locationss[2]
            _sub_district_codes = _locationss[1]
            _prv, _dis, _subdis = fn.prov_dis_subdis(_province_codes,_district_codes,_sub_district_codes)
            # print(int(_subdis))
            # print(_district_codes)
            addresss.append(_addresss)
            province_codes.append(int(_prv))
            district_codes.append(int(_dis))
            sub_district_codes.append(int(_subdis))

        except Exception as err:
            addresss.append('none')
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')

        try:
            _prices = soup.find('section', class_='mb-8 max-md:mb-8').find('p', class_='text-xl font-semibold mt-3').get_text().strip()\
                    .replace('฿','').replace('Sale Price:','').replace('ราคาประกาศขาย:','').replace('/เดือน','').replace(',','')
            # print(_prices)
            prices.append(int(_prices))
            range_of_house_prices.append(fn.get_range_of_price(_prices))
        except Exception as err:
            prices.append('none')
            range_of_house_prices.append(9)

        try:
            _bedrooms = soup.find('ul', class_='grid grid-cols-details-list-desktop gap-5 max-md:grid-cols-details-list-mobile lg:grid-cols-4 gap-x-2').get_text().split('ห้องนอน')[0]\
                .strip()

            # print(_bedrooms)
            bedrooms.append(_bedrooms)
        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms = soup.find('ul', class_='grid grid-cols-details-list-desktop gap-5 max-md:grid-cols-details-list-mobile lg:grid-cols-4 gap-x-2').get_text().split('ห้องน้ำ')[0]\
                .split('ห้องนอน')[1].strip()
            # print(_bathrooms)
            bathrooms.append(_bathrooms)

        except Exception as err:
            bathrooms.append('none')

        try:
            _detail = soup.find('div', class_='text-base property-listing-about').get_text().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')\
                .replace(',', '').replace('  ', '').replace('  ', '')
            # print(_detail)
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _map = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).get_text().strip())
            # print(_map)
            _latitudes = _map['props']['pageProps']['property']['gpsLat']
            _longtitudes = _map['props']['pageProps']['property']['gpsLong']
            # print(_longtitudes)
            latitudes.append(_latitudes)
            longtitudes.append(_longtitudes)

        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')
        # try:
        #     _locationss = soup.find('div', class_='container')
        #     # print(_locationss)
        #     # latitudes.append(_location['data-latitude'])
        #     # longtitudes.append(_location['data-longitude'])
        # except Exception as err:
        #     latitudes.append('none')
        #     longtitudes.append('none')

        try:
            _area_SQMs =soup.find('ul', class_='grid grid-cols-details-list-desktop gap-5 max-md:grid-cols-details-list-mobile lg:grid-cols-4 gap-x-2').get_text()\
                .split('ห้องน้ำ')[1].split('ตรม.')[0].strip()
            # print(_area_SQMs)
            area_SQMs.append(int(_area_SQMs))

        except Exception as err:
            area_SQMs.append('none')


        # try:
        #     _area_SQWs =soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split('เนื้อที่ดิน(ตร.วา):')[1].split('ตารางวา ')[0]
        #     # print(_area_SQWs)
        #     area_SQWs.append(int(_area_SQWs))
        #
        # except Exception as err:
        #     area_SQWs.append('none')

        try:
            # _num_floors =int(re.sub('[^0-9]', '',soup.find('ul', class_='grid grid-cols-details-list-desktop gap-5 max-md:grid-cols-details-list-mobile lg:grid-cols-4 gap-x-2').get_text().strip()\
            #      .split('ชั้น')[0].split('/ตรม.')[1].split()[0]))

            # _num_floors = soup.find('li', class_='undefined flex items-center ').find(text='**ฟังก์ชันบ้าน**').parent.parent.get_text().split('จำนวนชั้น :')[1].split('ชั้น')[0]
            # print(_num_floors)
            if type_id == 2:
                _num_floors = int(re.sub('[^0-9]', '', soup.find('ul', class_='grid grid-cols-details-list-desktop gap-5 max-md:grid-cols-details-list-mobile lg:grid-cols-4 gap-x-2').get_text().strip() \
                            .split('ชั้น')[0].split('/ตรม.')[1].split()[0]))
                floors.append(_num_floors)

                # print(floor_numbers)
            else:

                floors.append('none')
                # print(floors)
                # floor_numbers.append('none')

        except Exception as err:
            floors.append('none')
            # floor_numbers.append('none')

        try:
            # print(int(fn.get_source_id(web)))
            source_ids.append(int(fn.get_source_id(web)))

        except Exception as err:
            source_ids.append(0)

        # try:
        #     _seller_name = soup.find('div', class_='pd_contact_2').get_text().strip().replace('\n','').split('  ')[0]
        #     # print(_seller_name)
        #     seller_names.append(_seller_name)
        # except Exception as err:
        #     seller_names.append('none')
        #
        # try:
        #     _seller_tels = soup.find('div', class_='pd_contact_2').get_text().strip().replace('\n','').split('  ')[1].replace(' ','')
        #     # print(_seller_tels)
        #     seller_tels.append(_seller_tels)
        # except Exception as err:
        #     seller_tels.append("none")
        # try:
        #     _seller_emails = soup.find('div', class_='pd_contact_2').get_text().strip().replace('\n','').replace(' ','').split('คลิกเพื่อแสดงข้อมูลติดต่อ')[0]
        #     _seller_emails2 = _seller_emails.split()[2]
        #     # print(_seller_emails2)
        #     seller_emails.append(_seller_emails)
        # except Exception as err:
        #     seller_emails.append("none")

        try:
            if property_type[prop_type]["r_type"] == "ขาย":
                _sell_type_ids = int(1)

            else:
                _sell_type_ids = int(2)

            sell_type_ids.append(_sell_type_ids)
            # print(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))


    except Exception as err:
        # print(prop_url)
        print(err)


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

            # send line message on success.
            fn.send_message(date, web)
