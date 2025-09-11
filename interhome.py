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
# import geckodriver_autoinstaller
from fake_useragent import UserAgent
import platform
import ssl
import reic_function as fn

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()


# base_url = 'https://market.home.co.th/search?search=1&lat=15.90568418&lng=101.45705990&zoom=6&listingType=placeholder_sale_rent' \
#            '&propertyType=placeholder_type&beds=0,1,2,3,4,5,6&baths=0,1,2,3,4,5,6'


# base_url = 'https://propertyhub.in.th/placeholder_sale_rent%placeholder_type/placeholder_page'
base_url = 'https://www.interhome.co.th/result.php?resulttype=Search&proptype=placeholder_type&province=&district=&street=&price=&keyword=&plocate=both&propsell=placeholder_sale&proprent=placeholder_rent&page=placeholder_page'

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'interhome'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
    "home"          : {"type_id": 1, "route": "6", "property_sell_rent": 'Y', "property_rent": 'N', "start": 1, "end": 11},
    "condo"         : {"type_id": 2, "route": "9", "property_sell_rent": 'Y', "property_rent": 'N', "start": 1, "end": 8},
    "townhouse"     : {"type_id": 3, "route": "7", "property_sell_rent": 'Y', "property_rent": 'N', "start": 1, "end": 13},
    "home_rent"     : {"type_id": 1, "route": "6", "property_sell": 'N', "property_rent": 'Y', "start": 1, "end": 2},
    "condo_rent"    : {"type_id": 2, "route": "9", "property_sell": 'N', "property_rent": 'Y', "start": 1, "end": 4},
    "townhouse_rent": {"type_id": 3, "route": "7", "property_sell":'N', "property_rent": 'Y', "start": 1, "end": 3},
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


def get_data_datetime(soup_txt,_dateF=False):
    if _dateF:
        day = soup_txt.split(" ")[0]
        month = soup_txt.split(" ")[1]
        year = str(int(soup_txt.split(" ")[2]) - 543)
        if month in thai_abbr_months:
            month = str(thai_abbr_months.index(month)+1)
        else:
            if month in thai_full_months:
                month = str(thai_full_months.index(month)+1)
            else:
                month = "None"
        if month != "None":
            if len(month) == 1:
                month = "0" + month
        return day,month,year


def get_data(prop_url, type_id):
    # print(prop_url)
    Headers = {'User-Agent': ua.random}
    req = requests.get(prop_url, headers=Headers)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')
    # scripts = soup.find_all('script')
    # print(scripts)
    # for script in scripts:
    #     if '<script type="application/ld+json">' in str(script):
    #         temp = json.loads(str(script).replace('<script type="application/ld+json">', '').replace('</script>', ''))
            # print(temp)
            # if temp["@type"] == "Product":
            #     data = temp
                # print(data)

    try:
        webs.append(web)
        project_names.append("none")
        _o = int(0)

        try:
            _names = soup.find('h5', class_='text-center mb-0').get_text().strip()
            # print(_names)
            # _names = data["name"]
            names.append(_names)
        except Exception as err:
            names.append("none")

        try:
            _address = soup.find('div', class_='property-detail mt-20px').get_text().split('ที่ตั้ง :')[1].split('รายละเอียด')[0]
            _locationss =_address.trim().split()
            _locationss =  _address.trim().split()
            _province_codes  = _locationss[-1]
            _district_codes =  _locationss[-2]
            # print(_province_codes,_district_codes)
            _sub_district_codes = "none"
            _prv, _dis, _subdis = fn.prov_dis_subdis(_province_codes,_district_codes,_sub_district_codes)
            addresss.append(_address.trim())
            province_codes.append(int(_prv))
            # print(province_codes)
            district_codes.append(int(_dis))
            # print(district_codes)

            sub_district_codes.append(int(_subdis))
            # print(_prv,_dis,_subdis)

        except Exception as err:
            addresss.append('none')
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')


        try:
            # _prices = soup.find('span', class_='sc-3tpgds-0 cssmeV').get_text()
            # _prices_sale = soup.find('div', class_='bg-red d-flex justify-content-center align-items-center px-3').get_text().replace(',', '').replace('ขาย','').replace('บาท','').strip()
            # print(_prices)
            # _prices_rent = soup.find('div', class_='flex-align-center flex-wrap').get_text().split('ให้เช่าเดือนละ')[0].split('ที่จอดรถ')[1].strip().replace('-','')
            # print(_prices_rent)
            # # _price = data["offers"][0]["price"]
            if property_type[prop_type]["property_rent"] == "N":

                _prices = soup.find('div',class_='bg-red d-flex justify-content-center align-items-center px-3').get_text().replace(',', '').replace('ขาย', '').replace('บาท', '').strip()
            else:
                _prices =  soup.find('div', class_='flex-align-center flex-wrap').get_text().split('ให้เช่าเดือนละ')[0].split('ที่จอดรถ')[1].strip().replace('-', '')

            prices.append(int(_prices))
            range_of_house_prices.append(fn.get_range_of_price(int(_prices)))
            # print(prices)
            # print(range_of_house_prices)
        except Exception as err:
            prices.append('none')
            range_of_house_prices.append(9)
        #
        try:
            _bedrooms = soup.find('div', class_='flex-align-center flex-wrap').get_text().split('ห้องนอน')[0].split('จำนวนชั้น')[1].strip()
        #     print(_bedrooms)
            bedrooms.append(int(_bedrooms))
            # print(bedrooms)
        except Exception as err:
            bedrooms.append('none')
        #
        try:
            _bathrooms =soup.find('div', class_='flex-align-center flex-wrap').get_text().split('ห้องนอน')[1].split('ห้องน้ำ')[0].strip()
            # print(_bathrooms)
            # _bathrooms = soup.find('span', {'class': 'cfe8d274', 'aria-label': 'Baths'}).get_text().strip().replace(' ห้องน้ำ', '')
            bathrooms.append(int(_bathrooms))
        except Exception as err:
            bathrooms.append('none')
        #
        try:
            area_SQMs_ = "none"  # กำหนดค่าเริ่มต้น
            area_SQWs_ = "none"  # กำหนดค่าเริ่มต้น
            if property_type[prop_type]["route"] == "9":
                area_SQMs_ =soup.find('h5', class_='text-dark-blue').get_text().replace('ขนาด','').replace('ตร.ม.','').strip()
                # print(area_SQMs_)
                # area_SQMs.append(area_SQMs_)

            else:
                area_SQWs_ = soup.find('h5', class_='text-dark-blue').get_text().replace('ขนาด', '').replace('ตร.ว. ','').strip()
                # print(area_SQWs_)
                # area_SQWs.append(area_SQWs_)

            area_SQMs.append(area_SQMs_)
            area_SQWs.append(area_SQWs_)


        except Exception as err:
            area_SQWs.append('none')
            area_SQMs.append('none')

        # try:
        #     area_SQMs_ =soup.find('svg', class_='sc-ejnaz6-14 itMBpO').parent.get_text().replace('ตร.ม.','').strip()
        #     # print(area_SQMs_)
        #     area_SQMs.append(area_SQMs_)
        # except Exception as err:
        #     area_SQMs.append('none')

        try:
            _detail = soup.find('div', class_='property-detail mt-20px').get_text().split('รายละเอียด')[1].strip().replace('\n','')
            # print(_detail)
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _picture =soup.find('div', class_='img-16by9 holder').find('img', class_='img-click img-fluid')['src']
            # print(_picture)
            # _picture = soup.find('div', class_='sc-aicb4t-0 ieiBqw').find('picture', class_='sc-27ozv5-1 gAHpMv').find('source')['data-src']
            # print(_picture)
            # _picture = data["image"][0]
            house_pictures.append(_picture)
        except Exception as err:
            house_pictures.append('none')
        #
        try:
            source_ids.append(int(fn.get_source_id(web)))
            # print(source_ids)
        except Exception as err:
            source_ids.append(_o)

        try:
            _seller_names = soup.find('h4', class_='text-center').get_text().strip()
            # print(_seller_names)
            seller_names.append(_seller_names)
        except Exception as err:
            seller_names.append("none")

        try:
            _seller_tels = soup.find('h5', class_='text-center').parent.parent.parent.get_text().split('เบอร์ติดต่อ :')[1].split('Office')[0].strip()
            # print(_seller_tels)
            seller_tels.append(_seller_tels)
        except Exception as err:
            seller_tels.append("none")

        try:
            _floors = soup.find('div', class_='flex-align-center flex-wrap').get_text().split('จำนวนชั้น')[0].strip()
            # print(_floors)
            floors.append(_floors)
        except Exception as err:
            floors.append("none")

        # try:
        #     _floor_numbers = soup.find('div', class_='property-detail mt-20px').get_text().split('รายละเอียด')[1].split('อยู่ชั้น')[1].split()
        #     print(_floor_numbers)
        #     seller_tels.append(_floor_numbers)
        # except Exception as err:
        #     seller_tels.append("none")

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
            # _map = _seller_tels = json.loads(soup.find('script', {'type': 'application/json'}).get_text())['props']['pageProps']['listing']['nearbyProjects']['result'][0]['location']
            _map = soup.find('div', class_='box-map-per').find('small', class_='text-black-50').get_text().split('LatLong:')[1].split(',')

            # ['adDetail']\
            #                ['ad']['locations'][0]
            # print(_map)
            _latitudes = _map[0].strip()
            _longtitudes = _map[1].strip()
            # print(_latitudes,_longtitudes)
            latitudes.append(_latitudes)
            longtitudes.append(_longtitudes)

        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')

        try:
            if property_type[prop_type]["property_sell_rent"] == "N":
                _sell_type_ids = int(2)
            else:
                _sell_type_ids = int(1)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))

        floor_numbers.append('none')
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

    # sleep(randrange(2))


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
        get_data(link.strip(), type_id)
        # break


def save_list_links(prop_type):
    print("---------------------::  " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type].get("property_sell", '')  # ใช้ get() เพื่อดึงค่า
    list_type2 = property_type[prop_type].get("property_rent", '')  # ใช้ get() เพื่อดึงค่า
    req_url = base_url.replace("placeholder_type", route).replace("placeholder_sale", str(list_type)).replace("placeholder_rent", str(list_type2))

    # print(req_url)
    for i in tqdm(range(start_page, end_page)):
        Headers = {'User-Agent': ua.random}
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        r = requests.get(url, headers=Headers)
        # print(r.status_code)
        while r.status_code != 200:
            r = requests.get(url, headers=Headers)
        # print(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup)
        all_links = soup.find_all('a', class_='link-deco2')
        # print(all_links)
        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for j in all_links:
            _link = j['href']  # Use square brackets to access the 'href' attribute
            # print(_link)
            file_links.writelines('https://www.interhome.co.th/'+_link + "\n")
        file_links.close()
        sleep(wait_time)


# def extract_links(content):
#     links = []
#     for i in list( dict.fromkeys(re.findall("product-\d{1,10}",content))):
#         links.append("https://baan.kaidee.com/" + i)
#     return links

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

