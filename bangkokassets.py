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

ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()
base_url = 'https://www.bangkokassets.com/sellsearch?keyword=&req=full_type&pptid=placeholder_type&p=&c=&l=&ps=0&pe=6,588,750,000&rs=&re=&sarea=&earea=&sland=&eland=&pre=&st=&rec=1&limit=10&page=placeholder_page&order=0&map=0&fix=fixsell'

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web ="bangkokassets"
get_types = ['LINK','DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
    "home"      : { "type_id": 1, "route": "1", "full_type": 1, "start": 1, "end": 21 },
    "condo"     : { "type_id": 2, "route": "4", "full_type": 1, "start": 1, "end": 21 },
    "townhouse" : { "type_id": 3, "route": "3", "full_type": 1, "start": 1, "end": 21 },
    "home_rent"      : { "type_id": 1, "route": "1", "full_type": 2, "start": 1, "end": 5 },
    "condo_rent"     : { "type_id": 2, "route": "4", "full_type": 2, "start": 1, "end": 5 },
    "townhouse_rent" : { "type_id": 3, "route": "3", "full_type": 2, "start": 1, "end": 2 }
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
    list_type = property_type[prop_type]["full_type"]
    req_url = base_url.replace("placeholder_type", route).replace("full_type", str(list_type))


    for i in tqdm(range(start_page, end_page)):
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        req = requests.get(url)
        # print(req.status_code)
        soup = BeautifulSoup(req.text, 'html.parser')

        list = soup.find('div', {'class': 'rec_body1'}).find_all('div', {'class': 'rec_property_detail1'})
        # list = soup.find('div', class_='namedesw7').find_all('a', class_='namelink')
        # print(list)
        file_links = codecs.open(path_links + f"/link_{prop_type}.txt", "a+", "utf-8")
        for j in list:
            # print(j)
            _link = j.a['href']
            # print(_link)
            file_links.writelines(_link + "\n")
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

        try:
            _names = soup.find('div', class_='pd_Topic').get_text().strip().replace(' ','').replace(',','')
            # print(_names)
            names.append(_names)

        except Exception as err:
            names.append('none')

        try:
            _house_pictures = soup.find('img', id='CphBody_RptGallary_Image23_0')['src'].replace('..','')
            # print(_house_pictures)
            _link_house_pictures = "https://www.bangkokassets.com"+_house_pictures
            # print(_link_house_pictures)
            house_pictures.append(_link_house_pictures)

        except Exception as err:
            house_pictures.append('none')

        try:
            _project_name = _project_names = soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split()[4]
            if _project_name == 'ไม่มีข้อมูล':
                _project_name = 'none'
            project_names.append(_project_name)
        except Exception as error:
            project_names.append('none')

        try:
            _addresss = soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split('ที่อยู่:')[1].split('เนื้อที่ดิน(ตร.วา):')[0].replace(' ','').trim()
            _locationss = soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split('ที่อยู่:')[1].split('เนื้อที่ดิน(ตร.วา):')[0].trim()
            _province_codes = _locationss.split()[6].replace('จังหวัด','').trim()
            _district_codes = _locationss.split()[5].replace('อำเภอ','').trim()
            _sub_district_codes = _locationss.split()[4].replace('ตำบล','').trim()
            _prv, _dis, _subdis = fn.prov_dis_subdis(_province_codes,_district_codes,_sub_district_codes)
            # print(int(_prv))
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
            _prices = soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split('ราคา:')[1].split('บาท')[0].replace(',','')
            # print(_prices)
            prices.append(int(_prices))
            range_of_house_prices.append(fn.get_range_of_price(_prices))
        except Exception as err:
            prices.append('none')
            range_of_house_prices.append(9)

        try:
            _bedrooms = soup.find('div', class_='pd_property_detail_topic_detail spe').find(text='**ฟังก์ชันบ้าน**').parent.parent.get_text().split('ห้องนอน :')[1]\
                .split('ห้อง')[0]
            # print(_bedrooms)
            bedrooms.append(_bedrooms)
        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms = soup.find('div', class_='pd_property_detail_topic_detail spe').find(text='**ฟังก์ชันบ้าน**').parent.parent.get_text().split('ห้องห้องน้ำ :')[1] \
                .split('ห้อง')[0]
            # print(_bathrooms)
            bathrooms.append(_bathrooms)

        except Exception as err:
            bathrooms.append('none')

        try:
            _detail = soup.find('div', class_='pd_property_detail_topic_detail spe').get_text().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')\
                .replace(',', '').replace('  ', '').replace('  ', '')
            # print(_detail)
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _location = soup.find('div', class_='container').find_all('script', type='text/javascript')[3].text
            lo = _location.split('google.maps')[1].split('zoom')[0].replace('.LatLng','').replace('(','').replace(',','').replace(')','')
            _la = lo.split()
            _latitudes = _la[0]
            _longtitudes = _la[1]
            latitudes.append(_latitudes)
            longtitudes.append(_longtitudes)
        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')
        try:
            _locationss = soup.find('div', class_='container')
            # print(_locationss)
            # latitudes.append(_location['data-latitude'])
            # longtitudes.append(_location['data-longitude'])
        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')

        try:
            _area_SQMs =soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split('พื้นที่ใช้สอย(ตร.เมตร):')[1].split('ตารางเมตร')[0]
            # print(_area_SQMs)
            area_SQMs.append(int(_area_SQMs))

        except Exception as err:
            area_SQMs.append('none')


        try:
            _area_SQWs =soup.find('td', class_='pd_detail_title1').parent.parent.get_text().split('เนื้อที่ดิน(ตร.วา):')[1].split('ตารางวา ')[0]
            # print(_area_SQWs)
            area_SQWs.append(int(_area_SQWs))

        except Exception as err:
            area_SQWs.append('none')

        try:
            _num_floors = soup.find('div', class_='pd_property_detail_topic_detail spe').find(text='**ฟังก์ชันบ้าน**').parent.parent.get_text().split('จำนวนชั้น :')[1].split('ชั้น')[0]
            if type_id == 1 or type_id == 3:
                # print(_num_floors)
                floors.append('none')
                floor_numbers.append(_num_floors)
            else:

                floors.append(_num_floors)
                floor_numbers.append('none')
        except Exception as err:
            floors.append('none')
            floor_numbers.append('none')

        try:

            source_ids.append(int(fn.get_source_id(web)))

        except Exception as err:
            source_ids.append(0)

        try:
            _seller_name = soup.find('div', class_='pd_contact_2').get_text().strip().replace('\n','').split('  ')[0]
            # print(_seller_name)
            seller_names.append(_seller_name)
        except Exception as err:
            seller_names.append('none')

        try:
            _seller_tels = soup.find('div', class_='pd_contact_2').get_text().strip().replace('\n','').split('  ')[1].replace(' ','')
            # print(_seller_tels)
            seller_tels.append(_seller_tels)
        except Exception as err:
            seller_tels.append("none")
        try:
            _seller_emails = soup.find('div', class_='pd_contact_2').get_text().strip().replace('\n','').replace(' ','').split('คลิกเพื่อแสดงข้อมูลติดต่อ')[0]
            _seller_emails2 = _seller_emails.split()[2]
            # print(_seller_emails2)
            seller_emails.append(_seller_emails)
        except Exception as err:
            seller_emails.append("none")

        try:
            if property_type[prop_type]["full_type"] == 1:
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

            # check data
            fn.check_data(date, web)

            # send line message on success.
            fn.send_message(date, web)
