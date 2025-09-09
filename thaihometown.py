import sys
import os
import requests
import codecs
import re
import argparse
import pandas as pd
import reic_function as fn
from bs4 import BeautifulSoup
from tqdm import tqdm
from random import randint, randrange
from datetime import datetime,timedelta
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
import platform
# import schedule
import time
import ssl



# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

base_url = "https://www.thaihometown.com/search/?page=placeholder_page&FormType=Rent&Type=placeholder_type&Submit=Search"

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'thaihometown'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
    "home_rent"     : {"type_id": 1, "route": "Singlehouse", "r_type": "singlehouse", "start": 1, "end": 5},
    "condo_rent"    : {"type_id": 2, "route": "Condominiem", "r_type": "condo", "start": 1, "end": 5},
    "townhouse_rent": {"type_id": 3, "route": "Townhouse", "r_type": "townhouse", "start": 1, "end": 5},
    "Townhome_rent": {"type_id": 3, "route": "Townhome", "r_type": "townhome", "start": 1, "end": 5}
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


def save_list_links(prop_type):
    print("---------------------::  " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    route_type = property_type[prop_type]["r_type"]
    req_url = base_url.replace("placeholder_type", route)

    # print(base_url)
    for i in tqdm(range(start_page, end_page)):
        Headers = {'User-Agent': ua.random}
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        # print(url)
        req = requests.get(url, headers=Headers)
        # print(req.status_code)
        while req.status_code != 200:
            req = requests.get(url, headers=Headers)

        all_links = extract_links(req.text, route_type)
        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for link in all_links:
            file_links.writelines(link + "\n")
        file_links.close()
        sleep(wait_time)


def extract_links(content, route_type):
    soup = BeautifulSoup(content, "html.parser")
    # datas = soup.find("div", class_="namedesw7").find_all("a", class_='namelink')
    datas = soup.find_all("div", class_="infoSP")
    links = []
    for data in datas:
        a_tag = data.find("a", href=True)
        if a_tag and route_type in a_tag['href']:
            links.append(a_tag['href'])
    return links


def loop_links(prop_type):
    file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        link = links[i]
        get_data(link.strip(), type_id, ID)
        # break
        sleep(0.5)



def convert(content):
    # print(content)
    result = ''
    for char in content:
        asciichar = char.encode('ascii', errors="backslashreplace")[2:]
        if asciichar == '':
            utf8char = char.encode('utf8')
        else:
            try:
                hexchar = asciichar.decode('hex')
            except:
                #print asciichar
                utf8char = ' '
            try:
                utf8char = hexchar.encode('utf-8')
            except:
                #print hexchar
                utf8char = ' '
            #print utf8char

        result = result + utf8char
        #print result
    return result

def get_data(prop_url, type_id, ID):
    Headers = {'User-Agent': ua.random}
    req = requests.get(prop_url, headers=Headers)
    req.encoding = "cp874"

    soup = BeautifulSoup(req.text, 'html.parser')

    try:
        project_names.append('none')
        floors.append('none')
        floor_numbers.append('none')

        try:
            name = soup.find('title').get_text().split('|')[0].strip().replace(',', '')
            names.append(name)
            # print(name)
        except Exception as err:
            names.append('none')

        # try:
        #     _province = soup.find(text="จังหวัดที่ตั้ง : ").parent.parent.get_text().strip().split("\n")[2]
        # except Exception as err:
        #     _province = 'none'

        try:
            _addresss = soup.find('div', id='divinListDetail').get_text().split('ราคา :')[0].split('จังหวัด :')[1].strip().replace('\n', '').replace('เขตที่ตั้ง','')\
            .replace('อำเภอ','').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            _province=_addresss.split(':')[0].replace(' ','').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            _district=_addresss.split(':')[1].replace(' ','').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            _sub_district= 'none'
            _addresss = _province + ' ' + _district
            _prv_code, _dis_code, _subdis_code = fn.prov_dis_subdis(_province, _district, _sub_district)
            province_codes.append(int(_prv_code))
            district_codes.append(int(_dis_code))
            sub_district_codes.append(int(_subdis_code))
            addresss.append(_addresss)


        except Exception as err:
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')
            addresss.append('none')

        # try:
        #     if _province == 'กรุงเทพ':
        #         _district = soup.find(text="เขตที่ตั้ง : ").parent.parent.get_text().strip().split("\n")[2]
        #     else:
        #         _district = soup.find(text="อำเภอที่ตั้ง : ").parent.parent.get_text().strip().split("\n")[2]
        # except Exception as err:
        #     _district = 'none'
        #
        # _sub_district = 'none'

        # try:
        #     _addresss = _province + ' ' + _district
        #     addresss.append(_addresss)
        # except Exception as err:
        #     addresss.append('none')
        #
        # try:
        #     _prv_code, _dis_code, _subdis_code = fn.prov_dis_subdis(_province, _district, _sub_district)
        #     province_codes.append(int(_prv_code))
        #     district_codes.append(int(_dis_code))
        #     sub_district_codes.append(int(_subdis_code))
        # except Exception as err:
        #     province_codes.append('none')
        #     district_codes.append('none')
        #     sub_district_codes.append('none')

        try:
            _price = soup.find('td', class_='table_set3PriceN').get_text().strip().split('\n')
            if _price[2] == '':
                _prices = int(re.sub('[^0-9]', '', _price[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()))
                prices.append(_prices)
            else:
                _prices = int(re.sub('[^0-9]', '', _price[2].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()))
                prices.append(_prices)

            range_of_house_prices.append(fn.get_range_of_price(_prices))
        except Exception as err:
            prices.append(0)
            range_of_house_prices.append(9)

        if type_id == 1 or type_id == 3:
            try:
                _area_SQMs = soup.find('div', id='divinListDetail').get_text().split('พื้นที่ใช้สอย :')[1].split('จังหวัด')[0].replace('ตารางเมตร','').replace('ตารางวา','').strip().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                # print(_area_SQMs)
                _area_SQWs = soup.find('div', id='divinListDetail').get_text().split('ขนาดพื้นที่ :')[1].split('พื้นที่ใช้สอย')[0].replace('ตารางเมตร','').replace('ตารางวา','').strip().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                # print(_area_SQWs)
            except Exception as err:
                _area_SQMs = 'none'
                _area_SQWs = 'none'

            area_SQMs.append(_area_SQMs)
            area_SQWs.append(_area_SQWs)
        else:
            try:
                _area_SQMs = soup.find('div', id='divinListDetail').get_text().split('พื้นที่ห้อง :')[1].split('จังหวัด')[0].replace('ตารางเมตร','').replace('ตารางวา','').strip().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                # print(_area_SQMs)
                _area_SQWs = 'none'
            except Exception as err:
                _area_SQMs = 'none'
                _area_SQWs = 'none'

            area_SQMs.append(_area_SQMs)
            area_SQWs.append(_area_SQWs)


        try:
            room = soup.find(text="จำนวนห้อง : ").parent.parent.get_text().strip().split('\n')[1].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(room)
        except Exception as err:
            room = 'none'

        try:
            _bedrooms = soup.find('div', id='divinListDetail').get_text().split('จำนวนห้อง :')[1].split('ห้องนอน')[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(_bedrooms)
            bedrooms.append(_bedrooms)
        except Exception as err:
            bedrooms.append('none')

        try:
            map = soup.find('div', class_='maps_google2').parent
            iframe = map.find("iframe")["src"].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(iframe)
            _latitudes=iframe.split('!3d')[1].split('!')[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(latitudes)
            _longtitudes=iframe.split('!2d')[1].split('!')[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(longtitudes)
            latitudes.append(_latitudes)
            longtitudes.append(_longtitudes)



            # bedrooms.append(_bedrooms)
        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')

        try:

            _bathrooms = soup.find('div', id='divinListDetail').get_text().split('ห้องน้ำ')[0].strip().replace('\n','').split(' ')[-1].replace('พร้อม','0').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()

            # print(_bathrooms)
            bathrooms.append(_bathrooms)

        except Exception as err:
            bathrooms.append('none')

        try:
            _garages = room.split(' ')[5]
            if _garages == 'คัน':
                _garages = room.split(' ')[4].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            garages.append(_garages)
        except Exception as err:
            garages.append('none')

        try:
            _detail = soup.find('div', class_='headtitle2').get_text().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()

            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _house_pictures = soup.find('div', {'id': 'divImg'}).find('img', {'class': 'images_show'})['src'].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            house_pictures.append("https://www.prakardproperty.com" + _house_pictures)
        except Exception as err:
            house_pictures.append('none')

        try:
            source_ids.append(fn.get_source_id(web))
        except Exception as err:
            source_ids.append('none')

        try:
            _post_date = soup.find('div', {'class': 'datedetail'}).find('bdo').get_text().strip()\
                .replace('|', '').replace('วันที่โพสต์', ' ').replace('อัพเดทล่าสุด', ' ').replace('\n', '')\
                .replace('   ', '').replace('  ', '').split(' ')

            _day = _post_date[1]
            _month = thai_full_months.index(str(_post_date[2])) + 1
            _year = int(_post_date[3]) - 543
            days.append(_day)
            months.append(_month)
            years.append(_year)
            post_dates.append(str(_year) + '-' + str(_month) + '-' + str(_day))
        except Exception as err:
            days.append('none')
            months.append('none')
            years.append('none')
            post_dates.append('none')


        try:
            _seller_names = soup.find('span', {'id': 'rName'}).get_text().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            seller_names.append(_seller_names)
        except Exception as err:
            seller_names.append('none')

        try:
            _seller_tels = soup.find('div', {'id': 'PhoneMember'}).get_text().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            seller_tels.append(_seller_tels)
        except Exception as err:
            seller_tels.append('none')


        sell_type_ids.append(2)
        seller_emails.append('none')
        # seller_id ยังไม่ได้ทำ รอคำตอบจาก RS ว่าได้ใช้งานหรือไม่
        seller_ids.append(0)
        # latitudes.append('none')
        # longtitudes.append('none')
        duplicates.append(0)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        house_links.append(prop_url)
        type_ids.append(int(type_id))
        completion_years.append('none')
        ids.append(ID)
        webs.append(web)
        date_times.append(date_now)
        room_numbers.append('none')

        # print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)

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