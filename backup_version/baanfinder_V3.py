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
web = "baanfinder"
base_url = "https://www.baanfinder.com/th/%E0%B8%82%E0%B8%B2%E0%B8%A2?placeholder_type&page=placeholder_page"

date = datetime(2025, 1, 27).strftime('%Y-%m-%d')
date_now = fn.get_date_now()
# property_type = {
#     "home"        : {"type_id": 1, "route": "types=บ้านเดี่ยว&types=บ้านแฝด", "property_sell_rent": 'ขาย', "start": 1, "end": 1},
#     "condo"       : {"type_id": 2, "route": "types=คอนโด", "property_sell_rent": 'ขาย', "start": 1, "end":1},
#     "townhouse"   : {"type_id": 3, "route": "types=ทาวน์เฮ้าส์-ทาวน์โฮม", "property_sell_rent": 'ขาย', "start": 1,"end":1},
#     "home_rent": {"type_id": 1, "route": "types=บ้านเดี่ยว&types=บ้านแฝด", "property_sell_rent": 'ให้เช่า', "start": 1, "end": 1},
#     "condo_rent": {"type_id": 2, "route": "types=คอนโด", "property_sell_rent": 'ให้เช่า', "start": 1, "end": 1},
#     "townhouse_rent": {"type_id": 3, "route": "types=ทาวน์เฮ้าส์-ทาวน์โฮม", "property_sell_rent": 'ให้เช่า', "start": 1, "end": 1}
# }
property_type = {
    "home": {"type_id": 1, "route": "types=บ้านเดี่ยว&types=บ้านแฝด", "property_sell_rent": 'ขาย', "start": 1,
             "end": 30},
    "condo": {"type_id": 2, "route": "types=คอนโด", "property_sell_rent": 'ขาย', "start": 1, "end": 70},
    "townhouse": {"type_id": 3, "route": "types=ทาวน์เฮ้าส์-ทาวน์โฮม", "property_sell_rent": 'ขาย', "start": 1,
                  "end": 30},
    # "home_rent": {"type_id": 1, "route": "types=บ้านเดี่ยว&types=บ้านแฝด", "property_sell_rent": 'ให้เช่า', "start": 1, "end": 30},
    # "condo_rent": {"type_id": 2, "route": "types=คอนโด", "property_sell_rent": 'ให้เช่า', "start": 1, "end": 100},
    # "townhouse_rent": {"type_id": 3, "route": "types=ทาวน์เฮ้าส์-ทาวน์โฮม", "property_sell_rent": 'ให้เช่า', "start": 1, "end": 30}
}
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

thai_full_months = [
    'มกราคม',
    'กุมภาพันธ์',
    'มีนาคม',
    'เมษายน'

    "ธ.ค.",
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
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type]["property_sell_rent"]
    # req_url = base_url.replace("placeholder_type", route)

    for i in tqdm(range(start_page, end_page)):
        url = f'https://www.baanfinder.com/th/{list_type}?{route}&page={i}'
        print(url)
        print(scraper.get(url).status_code)
        html = scraper.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        _listings = soup.find_all('div', class_='resEntry')

        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for j in _listings:
            _link = j.find('h3', class_="residence-name").find('a')['href']
            # file_links.writelines('https://www.baanfinder.com' + _link + "\n")
            file_links.writelines('https://www.baanfinder.com' + _link.strip() + "\n")
        file_links.close()
        sleep(0.4)


def loop_links(prop_type, scraper):
    file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "r", "utf-8")
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    ID = 0
    for i in tqdm(range(len(links))):
        ID += 1
        link = links[i]
        try:
            get_data(link.strip(), type_id, ID, scraper)
        except Exception as err:
            print('\n', link.strip())
        # break
        sleep(0.2)


def get_data(prop_url, type_id, ID, scraper):
    print(scraper.get(prop_url).status_code)
    html = scraper.get(prop_url).text
    try:
        ids.append(ID)
        soup = BeautifulSoup(html, 'html.parser')
        _o = int(0)

        try:
            webs.append(str(web))

            try:
                _name = str(soup.find('span', class_='res-title').get_text().strip())
                names.append(_name)
            except Exception as err:
                names.append("none")

            try:
                _project_names = str(soup.find('span', class_='type-n-group').find_all('a')[1].get_text().strip())
                project_names.append(_project_names)
            except Exception as err:
                project_names.append('none')

            try:
                # _location = soup.find('div', class_='province').get_text().strip().replace('\n', '').split(',')
                # _prv, _dis, _subdis = fn.prov_dis_subdis(_location[2], _location[1], _location[0])

                _location = soup.find('div', class_='province d-inline me-lg-2').get_text().replace('\n', '').replace(
                    ',', '')
                _locations = re.sub(r'\s+', ' ', _location).strip().split()
                # print(_locations)
                #     .strip().replace('\n', '').split(',')
                _prv, _dis, _subdis = fn.prov_dis_subdis(_locations[-1], _locations[-2], _locations[-3])
                # print(_locations[-1], _locations[-2], _locations[-3])
                # print(_prv, _dis, _subdis)

                addresss.append(_locations[-1] + " " + _locations[-2] + " " + _locations[-3])
                province_codes.append(int(_prv))
                district_codes.append(int(_dis))
                sub_district_codes.append(int(_subdis))
                print(addresss)
                print(province_codes, district_codes, sub_district_codes)
            except Exception as err:
                addresss.append('none')
                province_codes.append(_o)
                district_codes.append(_o)
                sub_district_codes.append(_o)

            try:
                _price = int(re.sub('[^0-9]', '', soup.find('div', class_='post-type').find('span',
                                                                                            class_='price').get_text().strip()))
                prices.append(_price)
                range_of_house_prices.append(fn.get_range_of_price(_price))
            except Exception as err:
                prices.append(_o)
                range_of_house_prices.append(9)

            try:
                area_SQWs.append(soup.find(text='ตร.ว.\n').previous.strip())
            except Exception as err:
                area_SQWs.append('none')

            try:
                area_SQMs.append(soup.find(text='ม.').previous.strip())
            except Exception as err:
                area_SQMs.append('none')

            room_numbers.append('none')

            try:
                if property_type[prop_type]["property_sell_rent"] == "ขาย":
                    _sell_type_ids = int(1)
                else:
                    _sell_type_ids = int(2)
                sell_type_ids.append(_sell_type_ids)
            except Exception as err:
                sell_type_ids.append(int(1))

            try:
                _bedrooms = soup.find('div', class_='quick-summary').find('i',
                                                                          class_='bf bf-icon-bed tip').parent.next_sibling.replace(
                    '\n', '').replace(':', '')
                bedrooms.append(int(_bedrooms))
            except Exception as err:
                bedrooms.append('none')

            try:
                _bathrooms = soup.find('div', class_='quick-summary').find('i',
                                                                           class_='bf bf-icon-bath tip').parent.next_sibling.replace(
                    '\n', '').replace(':', '')
                bathrooms.append(int(_bathrooms))
            except Exception as err:
                bathrooms.append('none')

            try:
                _garages = soup.find('div', class_='quick-summary').find('i',
                                                                         class_='fa fa-car tip').parent.next_sibling.replace(
                    '\n', '').replace(':', '')
                garages.append(int(_garages))
            except:
                garages.append('none')

            try:
                _detail = soup.find("div", class_='detailedInfo').find('div', class_='detailedInfo').text.replace(',',
                                                                                                                  '').replace(
                    '\n', ' ').replace('\r', ' ').replace('\t', ' ')
                details.append(_detail)
            except Exception as err:
                details.append('none')

            try:
                _location = soup.find('iframe', width='100%', height='400')['src'].split('&')
                for i in _location:
                    if not str(i).find('q='):
                        latitudes.append(i.replace('q=', '').split(',')[0].strip())
                        longtitudes.append(i.replace('q=', '').split(',')[1].strip())
            except Exception as err:
                latitudes.append('none')
                longtitudes.append('none')

            duplicates.append(_o)
            news.append(int(1))
            cross_webs.append('none')
            cross_refs.append('none')

            try:
                house_pictures.append(soup.find('img', {'u': 'image'})['src2'])
            except Exception as err:
                house_pictures.append('none')

            try:
                source_ids.append(int(fn.get_source_id(web)))
            except Exception as err:
                source_ids.append(_o)

            house_links.append(prop_url)
            type_ids.append(int(type_id))

            try:
                seller_names.append(
                    str(soup.find('span', class_='reveal-contact-label-section').next_sibling.replace('\n', '').replace(
                        ':',
                        '')))
            except Exception as err:
                seller_names.append('none')

            try:
                seller_tels.append(str(soup.find('span', class_='js-reveal-phone').a.text.replace('-', '')))
            except Exception as err:
                seller_tels.append('none')

            seller_emails.append('none')
            # seller_id ยังไม่ได้ทำ รอคำตอบจาก RS ว่าได้ใช้งานหรือไม่
            seller_ids.append(_o)

            try:
                _find_floor = soup.find('div', class_='address-details').get_text().replace('\n', '  ').replace('\r',
                                                                                                                '  ').strip()
                _find_floor = _find_floor.replace('  ', ' ').split(' ')
                num_floor = 'none'
                for i in range(len(_find_floor)):
                    if _find_floor[i] == 'ชั้น':
                        num_floor = int(_find_floor[i + 1].replace(',', '').strip())

                if type_id == 1 or type_id == 3:
                    floors.append('none')
                else:
                    floors.append(num_floor)

                floor_numbers.append('none')
            except Exception as err:
                floors.append('none')
                floor_numbers.append('none')

            try:
                completion_years.append(
                    soup.find('i', class_='bf bf-icon-construction fa-fw tip').parent.next_sibling.replace('\n',
                                                                                                           '').replace(
                        ':',
                        ''))
            except Exception as err:
                completion_years.append('none')

            try:
                _update_date = soup.find('div', class_='res-postDate').get_text().strip().replace("วันที่อัพเดท - ",
                                                                                                  "").replace('\n',
                                                                                                              '').split(
                    ' ')
                _day = _update_date[0]
                _month = thai_abbr_months.index(str(_update_date[1])) + 1
                _year = _update_date[2]
                days.append(int(_day))
                months.append(int(_month))
                years.append(int(_year))
                post_dates.append(str(_year) + '-' + str(_month) + '-' + str(_day))
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

    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)


if __name__ == '__main__':
    # GET LINK
    for prop_type in property_type:
        save_list_links(prop_type, scraper)
        # break

    # GET DATA
    _start_date = datetime.now()
    for prop_type in property_type:
        print("---------------------::  GET DATA " + prop_type + "  ::---------------------")
        loop_links(prop_type, scraper)
        # break

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

    _type_name = ''
    for type_name in property_type:
        _type_name += '_' + type_name

    property_list.to_csv(path_Files + '/' + web + _type_name + '.csv')
    print('Export', web, len(ids), 'Rows To CSV File Completed!!!! ')
    print('Start At ', _start_date)
    print('Success At ', datetime.now())
