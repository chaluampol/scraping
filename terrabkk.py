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
from time import sleep
from random import randint, randrange
from datetime import datetime,timedelta
from selenium import webdriver
from time import sleep
import cloudscraper
from fake_useragent import UserAgent
import platform
import time
import ssl

# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

base_url = "https://www.terrabkk.com/freepost/property-list/placeholder_page?sort_by=&search_keyword=&f-post_type=placeholder_sale_rent&f-house_type=placeholder_type&d-province_id=&d-amphur_id=&d-district_id=&f-sell_price=&f-area_id=&d-room_type=&f-areasize_sqm=&f-landarea_total_sqw=&f-bts_id=&f-mrt_id="

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'terrabkk'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {

    "home_one"  : {"type_id": 1, "route": "6", "property_sell_rent": 1, "start": 1, "end": 50},
    "home_two"  : {"type_id": 1, "route": "197", "property_sell_rent": 1, "start": 1, "end": 2},
    "condo"     : {"type_id": 2, "route": "7", "property_sell_rent": 1, "start": 1, "end": 6},
    "townhouse" : {"type_id": 3, "route": "9", "property_sell_rent": 1, "start": 1, "end": 13},

    "home_one_rent" : {"type_id": 1, "route": "6", "property_sell_rent": 4, "start": 1, "end": 10},
    "home_two_rent" : {"type_id": 1, "route": "197", "property_sell_rent": 4, "start": 1, "end": 1},
    "condo_rent"    : {"type_id": 2, "route": "7", "property_sell_rent": 4, "start": 1, "end": 31},
    "townhouse_rent": {"type_id": 3, "route": "9", "property_sell_rent": 4, "start": 1, "end": 3}
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

# ++++++++++++ CloudScraper +++++++++++++++++
rand = randint(1000, 10000)
browsers = ['chrome', 'firefox']
platforms = [{'platform': 'linux', 'mobile': False, 'desktop': True},
            {'platform': 'windows', 'mobile': False, 'desktop': True},
            {'platform': 'darwin', 'mobile': False, 'desktop': True},
            {'platform': 'android', 'mobile': True, 'desktop': False}]

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


def get_data(prop_url, type_id, ID,scraper):
    # Headers = {'User-Agent': ua.random}
    # req = scraper.get(prop_url, headers=Headers)
    # req.encoding = "utf-8"
    # soup = BeautifulSoup(req.text, 'html.parser')
    # print(scraper.get(prop_url).status_code)
    html = scraper.get(prop_url).text
    soup = BeautifulSoup(html, 'html.parser')

    try:
        ids.append(ID)
        webs.append(web)
        _o = int(0)

        try:
            name = soup.find("title").get_text().split(" - ")[0].strip()
            names.append(name)
        except Exception as err:
            names.append("none")

        try:
            project_names.append(soup.find('h1', class_='freepost-title').get_text().strip())
        except Exception as err:
            project_names.append('none')

        try:
            _address = soup.find('p', class_='freepost-loc').get_text().strip()
            addresss.append(_address)
        except Exception as err:
            addresss.append('none')
            # print("Error => address")

        try:
            _location = soup.find('p', class_='freepost-loc').get_text().strip().split(' ')
            _prv, _dis, _subdis = fn.prov_dis_subdis(_location[2], _location[1], _location[0])
            province_codes.append(int(_prv))
            district_codes.append(int(_dis))
            sub_district_codes.append(int(_subdis))
        except Exception as err:
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')
            # print("Error => prv")

        try:
            if property_type[prop_type]["property_sell_rent"] == 1:
                _price = float(re.sub('[^0-9]', '', soup.find("div", class_='col-sm sell').span.text.strip()))
            elif property_type[prop_type]["property_sell_rent"] == 4:
                _price = float(re.sub('[^0-9]', '', soup.find("div", class_='col-sm rent').span.text.strip()))
            prices.append(_price)
            range_of_house_prices.append(fn.get_range_of_price(int(_price)))
        except Exception as err:
            prices.append(_o)
            range_of_house_prices.append(9)

        try:
            data_row = soup.find("div", class_="row column-desc").find_all("p", class_="col-6 col-sm")
            try:
                # ตร.ว
                area_SQWs.append(int(re.sub('[^0-9]', '', data_row[1].get_text().strip())))
            except Exception as err:
                area_SQWs.append('none')
            try:
                # ตร.ม.
                area_SQMs.append(int(re.sub('[^0-9]', '', data_row[2].get_text().strip())))
            except Exception as err:
                area_SQMs.append('none')
            try:
                # ห้องนอน
                bedrooms.append(int(re.sub('[^0-9]', '', data_row[3].get_text().strip())))
            except Exception as err:
                bedrooms.append('none')
            try:
                # ห้องน้ำ
                bathrooms.append(int(re.sub('[^0-9]', '', data_row[4].get_text().strip())))
            except Exception as err:
                bathrooms.append('none')
        except Exception as err:
            area_SQWs.append('none')
            area_SQMs.append('none')
            bedrooms.append(_o)
            bathrooms.append(_o)
            # print("Error ==> room")

        try:
            garages.append(int(re.sub('[^0-9]', '',
                                    soup.find(text="จำนวนที่จอดรถ").parent.parent.find("div", class_="ssgldtext border-bottom mb-3").get_text().strip())))
        except:
            garages.append('none')

        try:
            _details = soup.find("div", class_='less-detail-div').get_text().strip().replace('  ', ' ').replace(',', ' ').replace('\n', ' ').replace('\r', ' ')
            details.append(_details)
        except Exception as err:
            details.append('none')

        try:
            latitudes.append(soup.find("div", class_="nearby fixed-height longdo")['data-lat'])
            longtitudes.append(soup.find("div", class_="nearby fixed-height longdo")['data-lng'])
        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')


        try:
            house_pictures.append(soup.find('img', {'data-u': 'image'})['src'])
        except Exception as err:
            house_pictures.append('none')

        try:
            source_ids.append(int(fn.get_source_id(web)))
        except Exception as err:
            source_ids.append(_o)


        try:
            seller_names.append(soup.find('p', class_='author-name text-center').get_text().strip())
        except Exception as err:
            seller_names.append('none')

        try:
            seller_tels.append(soup.find('p', title_='โทรหา').a['data-show'])
        except Exception as err:
            seller_tels.append('none')


        try:
            _update_date = soup.find('div', class_='item-share row').find_all(
                'a', class_='col-auto')[0].get_text().strip().replace(
                "อัพเดทล่าสุดเมื่อ ", "").replace('\n', '')
            _day = _update_date.split('/')[0]
            _month = _update_date.split('/')[1]
            _year = _update_date.split('/')[2]
            days.append(int(_day))
            months.append(int(_month))
            years.append(int(_year))
            post_dates.append(str(_year) + '-' + str(_month) + '-' + str(_day))
        except Exception as err:
            days.append('none')
            months.append('none')
            years.append('none')
            post_dates.append('none')
            # print("Error => date")


        try:
            num_floors = int(re.sub('[^0-9]', '', soup.find(text="จำนวนชั้น").parent.parent.find("div", class_="ssgldtext border-bottom mb-3").get_text().strip()))
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
            if property_type[prop_type]["property_sell_rent"] == 1:
                _sell_type_ids = int(1)
            else:
                _sell_type_ids = int(2)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))

        house_links.append(prop_url)
        type_ids.append(int(type_id))
        room_numbers.append('none')
        duplicates.append(_o)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        seller_emails.append('none')
        # seller_id ยังไม่ได้ทำ รอคำตอบจาก RS ว่าได้ใช้งานหรือไม่
        seller_ids.append(_o)
        completion_years.append('none')
        date_times.append(date_now)

        # print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)

    # sleep(randrange(2))



def loop_links(prop_type,scraper):
    file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        link = links[i]
        # get_data(link.strip(), type_id)
        try:
            get_data(link.strip(), type_id, ID,scraper)
        except Exception as err:
            print('\n', link.strip())
            print('ERROR!!! =>', err)
        # break


def save_list_links(prop_type,scraper):
    print("---------------------::  " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type]["property_sell_rent"]
    req_url = base_url.replace("placeholder_type", route).replace("placeholder_sale_rent", str(list_type))

    for i in tqdm(range(start_page, end_page)):
        Headers = {'User-Agent': ua.random}
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        # print(url)
        # r = requests.get(url, headers=Headers)
        # print(r.status_code)
        # while r.status_code != 200:
        #     r = requests.get(url, headers=Headers)
        r = scraper.get(url)  # เรียกแค่ครั้งเดียว!
        # print(r.status_code)
        if r.status_code == 200:
            html = r.text
            # soup = BeautifulSoup(html, 'html.parser')
            # print(soup)
        else:
            print(f"Request failed with status code: {r.status_code}")

        all_links = extract_links(r.text)
        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for link in all_links:
            file_links.writelines(link + "\n")
        file_links.close()
        sleep(wait_time)


def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    datas = soup.find("div", {"id": "property-col"}).find_all("div", {"class": "property-item"})
    links = []
    for data in datas:
        links.append(data.find("a")['href'])
    return links


if __name__ == '__main__':

    for get_type in get_types:
        if get_type == 'LINK':
            for prop_type in property_type:
                save_list_links(prop_type, scraper)
                # break

        if get_type == "DATA":
            _start_date = datetime.now()
            for prop_type in property_type:
                print("---------------------::  GET DATA " + prop_type + "  ::---------------------")
                # เรียกใช้ฟังก์ชัน reset_list() ที่แก้ไขแล้ว
                reset_list()
                loop_links(prop_type,scraper)

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
