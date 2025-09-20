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
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

base_url = "https://www.livinginsider.com/searchword/placeholder_type/placeholder_sale_type/placeholder_page/placeholder_full_type"
# ****** วันที่เก็บข้อมูล ****** #
web = "livinginsider"
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 9, 19).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()
_day = date_now.split("-")[2]
_month = date_now.split("-")[1]
_year = date_now.split("-")[0]

property_type = {
    "home": {"type_id": 1, "route": "Home", "sale_type": 'Buysell',"full_type": 'รวมประกาศ-ขาย-บ้าน.html', "start": 1, "end": 35},
    "condo": {"type_id": 2, "route": "Condo","sale_type": 'Buysell',"full_type": 'รวมประกาศ-ขาย-คอนโด.html', "start": 1, "end": 100},
    "townhouse": {"type_id": 3, "route": "Townhome","sale_type": 'Buysell', "full_type": 'รวมประกาศ-ขาย-ทาวน์เฮ้าส์-ทาวน์โฮม.html', "start": 1, "end": 20},
    "home_rent": {"type_id": 1, "route": "Home", "sale_type": 'Rent',"full_type": 'รวมประกาศ-เช่า-บ้าน.html', "start": 1, "end": 15},
    "condo_rent": {"type_id": 2, "route": "Condo","sale_type": 'Rent',"full_type": 'รวมประกาศ-เช่า-คอนโด.html', "start": 1, "end": 100},
    "townhouse_rent": {"type_id": 3, "route": "Townhome","sale_type": 'Rent', "full_type": 'รวมประกาศ-เช่า-ทาวน์เฮ้าส์-ทาวน์โฮม.html', "start": 1, "end": 10}
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
    route_type = property_type[prop_type]["full_type"]
    list_type = property_type[prop_type].get("sale_type", '')  # ใช้ get() เพื่อดึงค่า
    # list_type2 = property_type[prop_type].get("sale_type", '')  # ใช้ get() เพื่อดึงค่า
    req_url = base_url.replace("placeholder_type", route).replace("placeholder_full_type", route_type).replace("placeholder_sale_type", str(list_type))

    for i in tqdm(range(start_page, end_page)):
        # Headers = {'User-Agent': ua.random}
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        # print(url)
        session = requests.Session()
        session.headers.update({
            'User-Agent': ua.random
        })
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount("https://", HTTPAdapter(max_retries=retries))

        # req = requests.get(url, headers=Headers, timeout=10)
        req = session.get(url, timeout=10)
        _loop_time = 0
        while req.status_code != 200:
            req = session.get(url, timeout=10)
            _loop_time += 1
            if _loop_time == 10:
                break

        ###### ถถ้า loop ครบ 10 ครั้งแล้วยังไม่ได้ 200 ให้หลุดจาก function ทันที
        if _loop_time == 10 and req.status_code != 200:
            return 

        all_links = extract_links(req.text)
        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for link in all_links:
            file_links.writelines(link + "\n")
        file_links.close()
        sleep(wait_time)


def extract_links(content):
    soup = BeautifulSoup(content, "html.parser")
    # print(soup)
    datas = soup.find("div", class_="panel-body").find_all("div", class_='istock-list')
    # print(datas)
    links = []
    for data in datas:
        result = data.find('a')['href']
        if result != "https://www.livinginsider.com/bclick.php?banid=902":
            links.append(result)
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


def get_data(prop_url, type_id, ID):
    # Headers = {'User-Agent': ua.random}
    # sleep(0.9)

    session = requests.Session()
    session.headers.update({
        'User-Agent': ua.random
    })
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))

    # req = requests.get(prop_url, headers=Headers, timeout=10)
    req = session.get(prop_url, timeout=10)
    _loop_time = 0
    while req.status_code != 200:
        req = session.get(prop_url, timeout=10)
        # print('while', req.status_code)
        _loop_time += 1
        if _loop_time == 10:
            break

    ###### ถถ้า loop ครบ 10 ครั้งแล้วยังไม่ได้ 200 ให้หลุดจาก function ทันที
    if _loop_time == 10 and req.status_code != 200:
        return 


    req.encoding = "utf-8"

    soup = BeautifulSoup(req.text, 'html.parser')
    # print(soup.get_text())

    try:
        garages.append('none')
        # province_codes.append('none')
        # district_codes.append('none')
        # sub_district_codes.append('none')

        try:
            name = soup.find('title').get_text().split('|')[0].strip().replace(',', '')
            names.append(name)
        except Exception as err:
            names.append('none')

        try:
            project_name = soup.find('div', class_='detail-text-project').find('a').get_text().strip()
            if project_name == 'ไม่ระบุโครงการ':
                project_name = 'none'
            project_names.append(project_name)
        except Exception as err:
            project_names.append('none')

        try:
            _addresss = soup.find('div', class_='box-show-text-all-project').get_text().strip().replace(',', '').replace('\n', ' ').replace('\r', '').replace('\t', '')
            # print(_addresss)
            _province_codes = _addresss.split('จังหวัด')[1].split(' ')[0]
            _district_codes = _addresss.split('เขต')[1].split(' ')[0]
            _sub_district_codes = _addresss.split('แขวง')[1].split(' ')[0]

            _prv, _dis, _subdis = fn.prov_dis_subdis(_province_codes, _district_codes, _sub_district_codes)
            province_codes.append(int(_prv))
            district_codes.append(int(_dis))
            sub_district_codes.append(int(_subdis))
            addresss.append(_province_codes + ' ' + _district_codes + ' ' + _sub_district_codes)
            # print(addresss)
        except Exception as err:
            addresss.append('none')
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')


        try:
            _price = int(re.sub('[^0-9]', '', soup.find('span', class_='price-detail').get_text().strip().replace(",", "").replace('฿', '')))
            prices.append(_price)
            range_of_house_prices.append(fn.get_range_of_price(_price))
        except Exception as err:
            prices.append(0)
            range_of_house_prices.append(9)

        _prop_detail = ''
        _detail_prop_list = ''
        try:
            _prop_detail = soup.find('div', class_="body-detail-left").find('div', class_="detail-list-property")
            _detail_prop_list = _prop_detail.find_all('span', class_="detail-property-list-title")
        except Exception as err:
            _prop_detail = 'none'
            _detail_prop_list = 'none'
        
        try:
            _area_SQWs = 'none'
            for ii in _detail_prop_list:
                if ii.find(string=re.compile(r'ขนาดที่ดิน')) != None:
                    _area_SQWs = ii.find(string=re.compile(r'ขนาดที่ดิน')).parent.parent.find('span', class_="detail-property-list-text").get_text().strip().split(" ")[0]
            area_SQWs.append(_area_SQWs.strip())
        except Exception as err:
            area_SQWs.append('none')

        try:
            _area_SQMs = 'none'
            for ii in _detail_prop_list:
                if ii.find(string=re.compile(r'พื้นที่ใช้สอย')) != None:
                    _area_SQMs = ii.find(string=re.compile(r'พื้นที่ใช้สอย')).parent.parent.find('span', class_="detail-property-list-text").get_text().strip().split(" ")[0]
            area_SQMs.append(_area_SQMs.strip())
        except Exception as err:
            area_SQMs.append('none')

        try:
            _bedrooms = 'none'
            for ii in _detail_prop_list:
                if ii.find(string=re.compile(r'ห้องนอน')) != None:
                    _bedrooms = ii.find(string=re.compile(r'ห้องนอน')).parent.parent.find('span', class_="detail-property-list-text").get_text().strip().split(" ")[0]
                    if _bedrooms == 'ห้องสตูดิโอ':
                        _bedrooms = 1
            bedrooms.append(_bedrooms.strip())
        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms = 'none'
            for ii in _detail_prop_list:
                if ii.find(string=re.compile(r'ห้องน้ำ')) != None:
                    _bathrooms = ii.find(string=re.compile(r'ห้องน้ำ')).parent.parent.find('span', class_="detail-property-list-text").get_text().strip().split(" ")[0]
            bathrooms.append(_bathrooms.strip())
        except Exception as err:
            bathrooms.append('none')

        try:
            _floor_numbers = 'none'
            for ii in _detail_prop_list:
                if ii.find(string=re.compile(r'จำนวนชั้น')) != None:
                    _floor_numbers = ii.find(string=re.compile(r'จำนวนชั้น')).parent.parent.find('span', class_="detail-property-list-text").get_text().strip().split(" ")[0]
            floor_numbers.append(_floor_numbers.strip())
        except Exception as err:
            floor_numbers.append('none')

        try:
            _floors = 'none'
            for ii in _detail_prop_list:
                if ii.find(string=re.compile(r'ชั้นที่')) != None:
                    _floors = ii.find(string=re.compile(r'ชั้นที่')).parent.parent.find('span', class_="detail-property-list-text").get_text().strip().split(" ")[0]
            floors.append(_floors.strip())
        except Exception as err:
            floors.append('none')

        try:
            _detail = soup.find('div', class_='wordwrap-box').get_text().strip()\
                .replace('\n', ' ').replace('\r', '').replace('\t', '').replace(',', '').replace('  ', ' ')
            details.append(_detail.strip())
        except Exception as err:
            details.append('none')

        try:
            # _house_pictures = soup.find('div', class_='img-topic-dynamic').find('img', class_='gridsection-1')['src']
            _house_pictures = soup.find("meta", property="og:image")["content"]
            house_pictures.append(_house_pictures)
        except Exception as err:
            house_pictures.append('none')

        try:
            _seller_names = soup.find('div', {'id': 'nameOwner'}).get_text().strip().replace('\n', ' ').replace('\r', '').replace('\t', '')
            seller_names.append(_seller_names)
        except Exception as err:
            seller_names.append('none')

        try:
            _map = soup.find('a', {'class': 'new-detail-gmap_'})['href'].split("=")[2]
            _latitudes = _map.split(",")[0]
            _longtitudes = _map.split(",")[1]

            latitudes.append(_latitudes)
            longtitudes.append(_longtitudes)
        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')

        try:
            _post_date = soup.find("span", class_="lv-small-font").get_text().replace("สร้างเมื่อ", "").strip().split(" ")[0]
            if _post_date != "None" or len(_post_date) > 4:
                if _post_date.count("days") != 0:
                    _post_date = (
                                datetime(int(_year), int(_month), int(_day)) - timedelta(int(_post_date[0]))).strftime(
                        '%Y-%m-%d')
                elif _post_date.count("week") != 0:
                    _post_date = (datetime(int(_year), int(_month), int(_day)) - timedelta(
                        int(_post_date[0]) * 7)).strftime(
                        '%Y-%m-%d')
                elif _post_date.count("month") != 0:
                    _post_date = (
                            datetime(int(_year), int(_month), int(_day)) - timedelta(int(_post_date[0]) * 30)).strftime(
                        '%Y-%m-%d')
                else:
                    _post_date = date_now
            else:
                _post_date = date_now
                post_dates.append(date_now)

            post_dates.append(_post_date)
            days.append(_post_date.split('-')[2])
            months.append(_post_date.split('-')[1])
            years.append(_post_date.split('-')[0])
        except Exception as err:
            post_dates.append('none')
            days.append('none')
            months.append('none')
            years.append('none')
        try:
            if property_type[prop_type]["sale_type"] == "Rent":
                _sell_type_ids = int(2)
            else:
                _sell_type_ids = int(1)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))


        source_ids.append(fn.get_source_id(web))
        seller_tels.append('none')
        # sell_type_ids.append(2)
        seller_emails.append('none')
        # seller_id ยังไม่ได้ทำ รอคำตอบจาก RS ว่าได้ใช้งานหรือไม่
        seller_ids.append(0)
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



if __name__ == "__main__":
    for get_type in get_types:
        # GET LINK
        if get_type == 'LINK':
            for prop_type in property_type:
                save_list_links(prop_type)
                # break
                
        # GET DATA
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