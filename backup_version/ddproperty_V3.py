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

# +++++++++++++ วันที่เก็บข้อมูล +++++++++++++ #
web = 'ddproperty'
date = datetime(2023, 6, 13).strftime('%Y-%m-%d')
date_now = fn.get_date_now()
_day = date_now.split("-")[2]
_month = date_now.split("-")[1]
_year = date_now.split("-")[0]

property_type = {
     # 'home'          : {'type_id': 1, 'type_value': 'B', 'route': 'BUNG', "property_sell_rent": 'รวมประกาศขาย', 'start': 1, 'end': 50},
     # 'condo'         : {'type_id': 2, 'type_value': 'N', 'route': 'CONDO', "property_sell_rent": 'รวมประกาศขาย', 'start': 1, 'end': 75},
     # 'townhouse'     : {'type_id': 3, 'type_value': 'T', 'route': 'TOWN', "property_sell_rent": 'รวมประกาศขาย', 'start': 1, 'end': 25},
     # 'home_rent'     : {'type_id': 1, 'type_value': 'B', 'route': 'BUNG', "property_sell_rent": 'รวมประกาศให้เช่า', 'start': 1, 'end': 30},
     'condo_rent'    : {'type_id': 2, 'type_value': 'N', 'route': 'CONDO', "property_sell_rent": 'รวมประกาศให้เช่า', 'start': 1, 'end': 2},
     # 'townhouse_rent': {'type_id': 3, 'type_value': 'T', 'route': 'TOWN', "property_sell_rent": 'รวมประกาศให้เช่า', 'start': 1, 'end': 20},
}

# ++++++++++++ CloudScraper +++++++++++++++++
rand = randint(1000, 30000)
browsers = ['chrome', 'firefox']
platforms = [{'platform': 'linux', 'mobile': False, 'desktop': True},
             {'platform': 'windows', 'mobile': False, 'desktop': True},
             {'platform': 'darwin', 'mobile': False, 'desktop': True},
             {'platform': 'android', 'mobile': True, 'desktop': False}]

rand_browser = browsers[randint(0, 1)]
rand_platform = platforms[randint(0, 3)]

scraper = cloudscraper.create_scraper(
    allow_brotli=False,
    browser={
        'browser': rand_browser,
        'platform': rand_platform['platform'],
        'desktop': rand_platform['desktop'],
        'mobile': rand_platform['mobile']
    },
    delay=rand,
    interpreter='nodejs',
    captcha={
        'provider': '2captcha',
        'api_key': '' #'8681c6f73588b47641ad9ec221562814'
    }
)

# +++++++++++++ ประเภททรัพย์ +++++++++++++ #
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

if not os.path.isdir('links/' + date):
    os.mkdir('links/' + date)
path_links = 'links/' + date + '/' + web
if not os.path.isdir(path_links):
    os.mkdir(path_links)

if not os.path.isdir('Files/' + date):
    os.mkdir('Files/' + date)
path_Files = 'Files/' + date + '/' + web
if not os.path.isdir(path_Files):
    os.mkdir(path_Files)

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


def save_list_links(prop_type, scraper):
    print("---------------------::  GET LINK " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    type_value = property_type[prop_type]["type_value"]
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type]["property_sell_rent"]

    # for t in property_sell_rent:
    #     print("------------------:: ", t, " ::---------------------------")
    for i in tqdm(range(int(start_page), int(end_page))):
        url = f'https://www.ddproperty.com/{list_type}/{i}?property_type={type_value}&property_type_code[]={route}&sort=date&order=desc'
        print(scraper.get(url).status_code)

        req = scraper.get(url).text
        soup = BeautifulSoup(req, 'html.parser')
        _listings = soup.find_all('div', class_='listing-card')

        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for j in _listings:
            _link = j.find('a', class_='nav-link')['href']
            file_links.writelines(_link + "\n")
            # break
        file_links.close()
        sleep(0.3)
        # break


def loop_links(prop_type, scraper, ID=0):
    file_links = codecs.open(path_links + f'/links_{prop_type}.txt', 'r', 'utf-8')
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    for j in tqdm(range(len(links))):
        ID += 1
        link = links[j]
        try:
            get_data(link.strip(), type_id, ID, scraper)
        except Exception as err:
            print('\n', link.strip())
        # break


def get_data(prop_url, type_id, ID, scraper):
    print(scraper.get(prop_url).status_code)
    html = scraper.get(prop_url).text
    try:
        soup = BeautifulSoup(html, 'html.parser')
        ids.append(ID)
        webs.append(web)
        house_links.append(prop_url)
        type_ids.append(type_id)
        garages.append('none')
        duplicates.append(0)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        room_numbers.append('none')
        seller_emails.append('none')
        seller_ids.append(0)
        date_times.append(date_now)

        try:
            name = soup.find('h1', {'class': 'h2 text-transform-none', 'itemprop': 'name'}).get_text().strip()\
                .replace('\n', '').replace('\r', '').replace('  ', '')
            names.append(name)
        except Exception as err:
            names.append('none')


        try:
            _project_name = soup.find('div', {'id': 'details'}).find(text='เจ้าของโครงการ').parent.parent.find_next('td').get_text().strip()\
                .replace('\n', '').replace('\r', '')
            if _project_name == 'ไม่มีข้อมูล':
                _project_name = 'none'
            project_names.append(_project_name)
        except Exception as error:
            project_names.append('none')


        try:
            _address = soup.find('div', class_='listing-address').find('span', {'itemprop': 'streetAddress'}).get_text().strip().replace(',', '')
            _addresss = _address.split(' ')
            _subdistrict = _addresss[len(_addresss) - 3]
            _district = _addresss[len(_addresss) - 2]
            _province = _addresss[len(_addresss) - 1]

            _prrovince_code, _district_code, _subdistrict_code = fn.prov_dis_subdis(_province, _district, _subdistrict)

            addresss.append(_address)
            province_codes.append(_prrovince_code)
            district_codes.append(_district_code)
            sub_district_codes.append(_subdistrict_code)
        except Exception as err:
            addresss.append(0)
            province_codes.append(0)
            district_codes.append(0)
            sub_district_codes.append(0)


        try:
            _price = soup.find('span', class_='element-label price', itemprop='price')['content']
            prices.append(_price)
            range_of_house_prices.append(fn.get_range_of_price(_price))
        except Exception as err:
            prices.append(0)
            range_of_house_prices.append(9)

        try:
            _area_SQMs = soup.find('tr', class_='property-attr floor-area').find('td', class_='value-block').get_text().strip() \
                .replace('\n', '').replace('\r', '').replace(' ', '').replace('ตร.ม.', '')
            if _area_SQMs == 'ไม่มีข้อมูล':
                _area_SQMs = 'none'
            area_SQMs.append(_area_SQMs)
        except Exception as err:
            area_SQMs.append('none')

        try:
            _area_SQWs = soup.find('div', id='details').find(text='ขนาดที่ดิน').parent.parent.find_next(
                'td').get_text().strip()
            if _area_SQWs == 'ไม่มีข้อมูล':
                _area_SQWs = 'none'
            area_SQWs.append(_area_SQWs)
        except Exception as error:
            area_SQWs.append('none')

        try:
            if property_type[prop_type]["property_sell_rent"] == "รวมประกาศขาย":
                _sell_type_ids = int(1)
            else:
                _sell_type_ids = int(2)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))

        try:
            _bedrooms = soup.find('div', class_='property-info-element beds').get_text().strip()
            bedrooms.append(_bedrooms)
        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms = soup.find('div', class_='property-info-element baths').get_text().strip()
            bathrooms.append(_bathrooms)
        except Exception as err:
            bathrooms.append('none')

        try:
            _detail = soup.find('div', class_='listing-details-text').get_text()\
                .replace('รายละเอียดเพิ่มเติม', '').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')\
                .replace(',', '').replace('  ', '')
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _location = soup.find('div', id='map-canvas')
            latitudes.append(_location['data-latitude'])
            longtitudes.append(_location['data-longitude'])
        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')



        try:
            num_floors = soup.find(text='ชั้น').parent.parent.find_next('td').get_text().strip().replace('ไม่มีข้อมูล', 'none')
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
            _house_pictures = soup.find('span', class_='gallery-item image').img['src']
            house_pictures.append(_house_pictures)
        except Exception as err:
            house_pictures.append('none')

        try:
            source_ids.append(int(fn.get_source_id(web)))
        except Exception as err:
            source_ids.append(0)


        try:
            _seller_name = soup.find('div', class_='list-group-item-heading').find('a').text.strip()
            seller_names.append(_seller_name)
        except Exception as err:
            seller_names.append('none')

        try:
            _seller_tels = soup.find("span", {"class": "agent-phone-number"})['data-mobile']
            seller_tels.append(_seller_tels)
        except Exception as err:
            seller_tels.append("none")

        try:
            _completion_years = soup.find('tr', class_='completion-year').get_text().strip()\
                .replace('\n', '').replace('\r', '').replace('ปีที่สร้างเสร็จ', '')
            if _completion_years == 'ไม่มีข้อมูล':
                _completion_years = 'none'
            completion_years.append(_completion_years)
        except Exception as err:
            completion_years.append('none')

        try:
            _post_date = soup.find(text="ลงประกาศเมื่อ").parent.parent.find_next("div").find_next("div").contents[0]
            if _post_date != "None":
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


        # print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)



if __name__ == '__main__':
      # GET LINK
    for prop_type in property_type:
        save_list_links(prop_type, scraper)
       # break

     # GET DATA
    # _start_date = datetime.now()
    # for prop_type in property_type:
    #     print("---------------------::  GET DATA " + prop_type + "  ::---------------------")
    #     loop_links(prop_type, scraper)
    #
    #     print('ids', len(ids))
    #     print('webs', len(webs))
    #     print('names', len(names))
    #     print('house_pictures', len(house_pictures))
    #     print('project_names', len(project_names))
    #     print('addresss', len(addresss))
    #     print('province_codes', len(province_codes))
    #     print('district_codes', len(district_codes))
    #     print('sub_district_codes', len(sub_district_codes))
    #     print('prices', len(prices))
    #     print('range_of_house_prices', len(range_of_house_prices))
    #     print('area_SQMs', len(area_SQMs))
    #     print('area_SQWs', len(area_SQWs))
    #     print('floor_numbers', len(floor_numbers))
    #     print('floors', len(floors))
    #     print('sell_type_ids', len(sell_type_ids))
    #     print('source_ids', len(source_ids))
    #     print('bedrooms', len(bedrooms))
    #     print('bathrooms', len(bathrooms))
    #     print('garages', len(garages))
    #     print('details', len(details))
    #     print('latitudes', len(latitudes))
    #     print('longtitudes', len(longtitudes))
    #     print('duplicates', len(duplicates))
    #     print('news', len(news))
    #     print('cross_webs', len(cross_webs))
    #     print('cross_refs', len(cross_refs))
    #     print('days', len(days))
    #     print('months', len(months))
    #     print('years', len(years))
    #     print('post_dates', len(post_dates))
    #     print('seller_names', len(seller_names))
    #     print('seller_tels', len(seller_tels))
    #     print('seller_emails', len(seller_emails))
    #     print('seller_ids', len(seller_ids))
    #     print('room_numbers', len(room_numbers))
    #     print('house_links', len(house_links))
    #     print('type_ids', len(type_ids))
    #     print('completion_years', len(completion_years))
    #     print('date_times', len(date_times))
    #
    #     property_list = pd.DataFrame({
    #         'ID': ids,
    #         'web': webs,
    #         'name': names,
    #         'project_name': project_names,
    #         'address': addresss,
    #         'subdistrict_code': sub_district_codes,
    #         'district_code': district_codes,
    #         'province_code': province_codes,
    #         'price': prices,
    #         'range_of_house_price': range_of_house_prices,
    #         'area_SQM': area_SQMs,
    #         'area_SQW': area_SQWs,
    #         'floor_number': floor_numbers,
    #         'floor': floors,
    #         'room_number': room_numbers,
    #         'bedroom': bedrooms,
    #         'bathroom': bathrooms,
    #         'garage': garages,
    #         'latitude': latitudes,
    #         'longtitude': longtitudes,
    #         'detail': details,
    #         'seller_name': seller_names,
    #         'seller_tel': seller_tels,
    #         'seller_email': seller_emails,
    #         'seller_id': seller_ids,
    #         'picture': house_pictures,
    #         'house_link': house_links,
    #         'type_id': type_ids,
    #         'sell_type_id': sell_type_ids,
    #         'source_id': source_ids,
    #         'duplicate': duplicates,  # 0
    #         'new': news,  # 1
    #         'cross_web': cross_webs,  # -1
    #         'cross_ref': cross_refs,  # str("None")
    #         'completion_year': completion_years,  # str("None")
    #         'year': years,
    #         'month': months,
    #         'day': days,
    #         'post_date': post_dates,
    #         'date_time': date_times,  # date
    #         'update_date': post_dates,
    #     })
    #
    #     _type_name = ''
    #     for type_name in property_type:
    #         _type_name += '_' + type_name
    #
    #
    #     property_list.to_csv(path_Files + '/' + web + _type_name + '.csv')
    #     print('Export', web, len(ids), 'Rows To CSV File Completed!!!! ')
    #     print('Start At ', _start_date)
    #     print('Success At ', datetime.now())
    #     # break
