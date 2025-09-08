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
from fake_useragent import UserAgent
import platform
import time
import ssl

# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()


# print('')




web = "baanfinder"
base_url = "https://www.baanfinder.com/th/%E0%B8%82%E0%B8%B2%E0%B8%A2?placeholder_type&page=placeholder_page"

# ****** วันที่เก็บข้อมูล ****** #
date = datetime(2021, 4, 5).strftime('%Y-%m-%d')
date_now = fn.get_date_now()
property_type = {
    "home"        : { "type_id" : 1, "route":"types=บ้านเดี่ยว&types=บ้านแฝด", "start":1, "end":3 },
    # "condo"       : { "type_id" : 2, "route":"types=คอนโด", "start":1, "end":10 },
    # "townhouse"   : { "type_id" : 3, "route":"types=ทาวน์เฮ้าส์-ทาวน์โฮม", "start":1, "end":10 }
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

if not os.path.isdir("links/" + date):
    os.mkdir("links/" + date)
path_links = "links/" + date + "/" + web
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


def get_data(prop_url, type_id):
    # print(prop_url)

    Headers = {'User-Agent': ua.random}

    req = requests.get(prop_url, headers=Headers)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')

    try:
        webs.append(str(web))

        try:
            name = soup.find("title").get_text().split(" - ")[0].strip()
            names.append(str(name))
        except Exception as err:
            names.append("none")


        try:
            project_names.append(str(soup.find('span', class_='type-n-group').find_all('a')[1].get_text().strip()))
        except Exception as err:
            project_names.append('none')

        try:
            address = soup.find_all('div', class_='province')[1].get_text().strip().replace('\n', ' ').replace('   ',
                                                                                                               ' ').replace(
                '  ', ' ')
            addresss.append(str(address))
        except Exception as err:
            address = 'none'
            addresss.append('none')

        try:
            _location = soup.find('div', class_='province').get_text().strip().replace('\n', '').split(',')
            _prv, _dis, _subdis = fn.prov_dis_subdis(_location[2], _location[1], _location[0])
            province_codes.append(_prv)
            district_codes.append(_dis)
            sub_district_codes.append(_subdis)
        except Exception as err:
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')

        try:
            _price = \
            soup.find('div', class_='post-type').find('span', class_='price').get_text().replace(',', '').split(' ')[0]
            prices.append(_price)
            range_of_house_prices.append(fn.get_range_of_price(_price))
        except Exception as err:
            prices.append('none')
            range_of_house_prices.append('none')

        try:
            area_SQWs.append(soup.find(text='ตร.ว.\n').previous.strip())
        except Exception as err:
            area_SQWs.append('none')

        try:
            area_SQMs.append(soup.find(text='ม.').previous.strip())
        except Exception as err:
            area_SQMs.append('none')

        floor_numbers.append('none')
        try:
            _find_floor = address.split(' ')
            _floor = 'none'
            for i in range(len(_find_floor)):
                if _find_floor[i] == 'ชั้น':
                    _floor = int(_find_floor[i + 1].replace(',', '').strip())
            floors.append(_floor)
        except Exception as err:
            floors.append('none')

        room_numbers.append('none')
        sell_type_ids.append(1)

        try:
            bedrooms.append(
                soup.find('i', class_='bf bf-icon-bed tip').parent.next_sibling.replace('\n', '').replace(':', ''))
        except Exception as err:
            bedrooms.append('none')

        try:
            bathrooms.append(
                soup.find('i', class_='bf bf-icon-bath tip').parent.next_sibling.replace('\n', '').replace(':', ''))
        except Exception as err:
            bathrooms.append('none')

        try:
            garages.append(
                soup.find('i', class_='fa fa-car tip').parent.next_sibling.replace('\n', '').replace(':', ''))
        except:
            garages.append('none')

        try:
            _detail = soup.find("div", class_='detailedInfo').find('div', class_='detailedInfo').text
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

        duplicates.append(0)
        news.append(1)
        cross_webs.append('none')
        cross_refs.append('none')

        try:
            house_pictures.append(soup.find('img', {'u': 'image'})['src2'])
        except Exception as err:
            house_pictures.append('none')

        try:
            source_ids.append(fn.get_source_id(web))
        except Exception as err:
            source_ids.append(0)

        house_links.append(prop_url)
        type_ids.append(type_id)

        try:
            seller_names.append(
                str(soup.find('span', class_='reveal-contact-label-section').next_sibling.replace('\n', '').replace(':',
                                                                                                                '')))
        except Exception as err:
            seller_names.append('none')

        try:
            seller_tels.append(str(soup.find('span', class_='js-reveal-phone').a.text.replace('-', '')))
        except Exception as err:
            seller_tels.append('none')

        seller_emails.append('none')
        # seller_id ยังไม่ได้ทำ รอคำตอบจาก RS ว่าได้ใช้งานหรือไม่
        seller_ids.append(0)

        try:
            completion_years.append(
                soup.find('i', class_='bf bf-icon-construction fa-fw tip').parent.next_sibling.replace('\n',
                                                                                                       '').replace(':',
                                                                                                                   ''))
        except Exception as err:
            completion_years.append('none')

        try:
            _update_date = soup.find('div', class_='res-postDate').get_text().strip().replace("วันที่อัพเดท - ",
                                                                                              "").replace('\n',
                                                                                                          '').split(' ')
            _day = _update_date[0]
            _month = thai_abbr_months.index(str(_update_date[1])) + 1
            _year = _update_date[2]
            days.append(_day)
            months.append(_month)
            years.append(_year)
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
    print("---------------------::  GET LINK " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    req_url = base_url.replace("placeholder_type", route)
    # print(req_url)
    Cookies =  {
        'verify': 'test',
        'BF_ERRORS': '',
        'BF_FLASH': '',
        'BF_SESSION': '',
        '_clck': 'kwzsf9',
        '__cf_bm': '9169a9b55dac0cce376228721f7a4d78b718898c-1617594625-1800-ASdYCwFvWkOjRQ+bEnHXuMnIbND0AJP5yS8s9bxo3+9ly2TCssnp60vsz18ts308c+5a/OHApK9QuRqWU1C1a2RdKcRw6U3TjN1a37HjHwzQRXxfOxPRv5kLdB+ZSVnPyQ==',
        '__cfduid': 'dee3557b7bfa8917f78efd2d702fe60451617594623',
        '_awl': '2.1617594821.0.4-b9fa8341-88d13e986c32c4d0ec62a692c2c0d3f9-6763652d617369612d6561737431-606a89c5-1',
        '_cbclose': '1',
        '_cbclose57999': '1',
        '_ctout57999': '1',
        '_ga': 'GA1.2.1654196905.1608532219',
        '_gat': '1',
        '_gid': 'GA1.2.628093288.1617594624',
        '_uid57999': '50C75DB6.9',
        'visit_time': '0'

    }

    for i in tqdm(range(start_page, end_page)):
        Headers = {'User-Agent': ua.random, 'cookie': 'verify=test; _ga=GA1.2.1654196905.1608532219; _clck=kwzsf9; __cfduid=dee3557b7bfa8917f78efd2d702fe60451617594623; _gid=GA1.2.628093288.1617594624; _cbclose=1; _cbclose57999=1; _uid57999=50C75DB6.9; _ctout57999=1; __cf_bm=9169a9b55dac0cce376228721f7a4d78b718898c-1617594625-1800-ASdYCwFvWkOjRQ+bEnHXuMnIbND0AJP5yS8s9bxo3+9ly2TCssnp60vsz18ts308c+5a/OHApK9QuRqWU1C1a2RdKcRw6U3TjN1a37HjHwzQRXxfOxPRv5kLdB+ZSVnPyQ==; _gat=1; _awl=2.1617594763.0.4-cc0533d7-88d13e986c32c4d0ec62a692c2c0d3f9-6763652d617369612d6561737431-606a898b-1'}
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))

        print(url)

        # r2 = requests.get(url, headers=Headers)
        r = requests.get(url, headers=Headers)

        print(r.headers)

        all_links = extract_links(r.text)
        file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
        for link in all_links:
            file_links.writelines(link + "\n")
        file_links.close()
        sleep(wait_time)

        break;

def extract_links(content):
    return list(set([ "https://www.baanfinder.com" + link for link in re.findall("/th/property/\d{1,10}_.*?ref=search-prop",content)]))


if __name__ == '__main__':
    # Get link
    for prop_type in property_type:
        save_list_links(prop_type)


    # # Get Data
    # for prop_type in property_type:
    #     print("---------------------::  GET DATA " + prop_type + "  ::---------------------")
    #     loop_links(prop_type)
    #     # break

    # print('ids', len(ids))
    # print('webs', len(webs))
    # print('names', len(names))
    # print('house_pictures', len(house_pictures))
    # print('project_names', len(project_names))
    # print('addresss', len(addresss))
    # print('province_codes', len(province_codes))
    # print('district_codes', len(district_codes))
    # print('sub_district_codes', len(sub_district_codes))
    # print('prices', len(prices))
    # print('range_of_house_prices', len(range_of_house_prices))
    # print('area_SQMs', len(area_SQMs))
    # print('area_SQWs', len(area_SQWs))
    # print('floor_numbers', len(floor_numbers))
    # print('floors', len(floors))
    # print('sell_type_ids', len(sell_type_ids))
    # print('source_ids', len(source_ids))
    # print('bedrooms', len(bedrooms))
    # print('bathrooms', len(bathrooms))
    # print('garages', len(garages))
    # print('details', len(details))
    # print('latitudes', len(latitudes))
    # print('longtitudes', len(longtitudes))
    # print('duplicates', len(duplicates))
    # print('news', len(news))
    # print('cross_webs', len(cross_webs))
    # print('cross_refs', len(cross_refs))
    # print('days', len(days))
    # print('months', len(months))
    # print('years', len(years))
    # print('post_dates', len(post_dates))
    # print('seller_names', len(seller_names))
    # print('seller_tels', len(seller_tels))
    # print('seller_emails', len(seller_emails))
    # print('seller_ids', len(seller_ids))
    # print('room_numbers', len(room_numbers))
    # print('house_links', len(house_links))
    # print('type_ids', len(type_ids))
    # print('completion_years', len(completion_years))
    # print('date_times', len(date_times))


    # property_list = pd.DataFrame({
    #     'ID': ids,
    #     'web': webs,
    #     'name': names,
    #     'project_name': project_names,
    #     'address': addresss,
    #     'subdistrict_code': sub_district_codes,
    #     'district_code': district_codes,
    #     'province_code': province_codes,
    #     'price': prices,
    #     'range_of_house_price': range_of_house_prices,
    #     'area_SQM': area_SQMs,
    #     'area_SQW': area_SQWs,
    #     'floor_number': floor_numbers,
    #     'floor': floors,
    #     'room_number': room_numbers,
    #     'bedroom': bedrooms,
    #     'bathroom': bathrooms,
    #     'garage': garages,
    #     'latitude': latitudes,
    #     'longtitude': longtitudes,
    #     'detail': details,
    #     'seller_name': seller_names,
    #     'seller_tel': seller_tels,
    #     'seller_email': seller_emails,
    #     'seller_id': seller_ids,
    #     'picture': house_pictures,
    #     'house_link': house_links,
    #     'type_id': type_ids,
    #     'sell_type_id': sell_type_ids,
    #     'source_id': source_ids,
    #     'duplicate': duplicates,  # 0
    #     'new': news,  # 1
    #     'cross_web': cross_webs,  # -1
    #     'cross_ref': cross_refs,  # str("None")
    #     'completion_year': completion_years,  # str("None")
    #     'year': years,
    #     'month': months,
    #     'day': days,
    #     'post_date': post_dates,
    #     'date_time': date_times,  # date
    #     'update_date': post_dates,
    # })
    #
    # property_list.to_csv(path_Files + '/' + web + '.csv')
    # print('Export', len(ids), 'Rows To CSV File Completed!!!! ')