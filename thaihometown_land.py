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
# from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
import platform
# import schedule
import time
import ssl



# set ssl
ssl._create_default_https_context = ssl._create_unverified_context
ua = UserAgent()

web = "thaihometownlind"
# base_url = "https://www.thaihometown.com/search/?page=placeholder_page&FormType=Sale&Type=placeholder_type&Submit=Search"
base_url ="https://www.thaihometown.com/search/?page=placeholder_page&FormType=Sale&Type=placeholder_type&Submit=Search"


# ****** วันที่เก็บข้อมูล ****** #
date = datetime(2025, 1, 31).strftime('%Y-%m-%d')
date_now = fn.get_date_now()
property_type = {
    "Land": {"type_id": 1, "route": "Land", "r_type": "land", "start": 368 ,"end": 490}
 # 355-366 #ผ่าน  45
# ไม่ผ่าน


















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
ref_code = []
webs = []
names = []
house_pictures = []
project_names = []
addresss = []
province = []
district = []
sub_district = []
province_codes = []
district_codes = []
sub_district_codes = []
prices = []
range_of_house_prices = []
area = []
area_rai = []
area_Ngan = []
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
        print(url)
        req = requests.get(url, headers=Headers)
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
    sleep(0.5)

    try:
        project_names.append('none')
        floors.append('none')
        floor_numbers.append('none')
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
        print(ids)
        webs.append(web)
        date_times.append(date_now)
        room_numbers.append('none')

        try:
            _ref_code = soup.find('div', class_ ='NoID').get_text().strip().replace("\n","").replace("No.","")
            print(_ref_code)
            ref_code.append(_ref_code)
        except Exception as err:
            ref_code.append('none')

        try:
            name = soup.find('title').get_text().split('|')[0].strip().replace(',', '')
            # print(name)
            names.append(name)
        except Exception as err:
            names.append('none')

        try:
            _latitude = soup.find('div', class_='maps_google2').parent.iframe['src'].split('!3d')[1].split('!')[0]
            latitudes.append(_latitude)
            print(_latitude)
        except Exception as err:
            latitudes.append('none')


        try:
            _longtitudes = soup.find('div', class_='maps_google2').parent.iframe['src'].split('!2d')[1].split('!')[0]
            longtitudes.append(_longtitudes)
            print(_longtitudes)
        except Exception as err:
            longtitudes.append('none')

        try:
            # _province = soup.find(text="จังหวัดที่ตั้ง : ").parent.parent.get_text().strip().split("\n")[2]
            _provinces = soup.find_all('a', class_='linkcity')[1].get_text().strip().replace('ตารางวา', '').replace('ตารางเมตร', '').replace('  ', '').replace(',', '')
            _provinces = re.sub(r'\d+', ' ', _provinces)
            province.append(_provinces)

            # print(_provinces)
        except Exception as err:
            province.append('none')

        try:
            _district = soup.find_all('a', class_='linkcity')[2].get_text().strip().replace('ตารางวา', '').replace('ตารางเมตร', '').replace('  ', '').replace(',', '')
            _district = re.sub(r'\d+', ' ', _district)
            district.append(_district)
        except Exception as err:
            district.append('none')

        try:
            _sub_district = soup.find_all('a', class_='linkcity')[3].get_text().strip().replace('ตารางวา', '').replace('ตารางเมตร', '').replace('  ', '').replace(',', '')
            _sub_district = re.sub(r'\d+', ' ', _sub_district)
            sub_district.append(_sub_district)
        except Exception as err:
            sub_district.append('none')

        try:
            _addresss = _provinces + ' ' + _district
            addresss.append(_addresss)
        except Exception as err:
            addresss.append('none')

        try:
            _prv_code, _dis_code, _subdis_code = fn.prov_dis_subdis(_provinces, _district, _sub_district)
            province_codes.append(int(_prv_code))
            district_codes.append(int(_dis_code))
            sub_district_codes.append(int(_subdis_code))
        except Exception as err:
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')

        try:
            _price = soup.find('td', class_='table_set3PriceN').get_text().strip().split('\n')
            if _price[2] == '':
                _prices = int(re.sub('[^0-9]', '', _price[0]))
                prices.append(_prices)
            else:
                _prices = int(re.sub('[^0-9]', '', _price[2]))
                prices.append(_prices)


            range_of_house_prices.append(fn.get_range_of_price(_prices))
        except Exception as err:
            prices.append(0)
            range_of_house_prices.append(9)


        try:
            _area = soup.find('div', class_='sqm_right').parent.parent.get_text().strip().replace('เนื้อที่รวม : ', '')
            if _area == '':
                _area = \
                soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split(
                    "ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('', '').replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace('\r', '').replace(',', '')
            # print(_area)
            area.append(_area)
        except AttributeError:
            _area = \
            soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split(
                "ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('', '').replace('\n', '').replace('\t', '').replace(
                'ขนาดที่ดิน', '').replace('\r', '').replace(',', '')
            print(_area)
            area.append(_area)
        except Exception as err:
            area.append('none')

        try:
            _area = soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split("ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('','') \
                .replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace('\r', '').replace(',', '')
            # print(_area)
            pattern = r'(\d+(?:\.\d+)?)\sไร่'  # Regular expression pattern to match the number in front of "ไร่"
            matches = re.findall(pattern, _area)  # Find all matches in the data
            # print(_area)
            # Print the extracted numbers
            for _area_rai in matches:
            # print(match)
            # _area_rai = _area.split('ตารางวา')

                print(_area_rai)
            area_rai.append(_area_rai)

        except Exception as err:
            area_rai.append('0')

        try:
            _area = soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split("ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('','') \
                .replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace('\r', '').replace(',', '')
            # _area_Ngan =_area.split('งาน')[0].split('ไร่')[1]
            pattern = r'(\d+(?:\.\d+)?)\sงาน'
            matches = re.findall(pattern, _area)  # Find all matches in the data
            # print(_area)
            # Print the extracted numbers
            for _area_Ngan in matches:
                # print(match)
                # _area_rai = _area.split('ตารางวา')

                print(_area_rai)
            # print(_area)
            # print(_area_Ngan)
            area_Ngan.append(_area_Ngan)
            print(area_Ngan)

        except Exception as err:
            area_Ngan.append('0')


        try:
            _area = soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split("ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('', '') \
                .replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace('\r', '').replace(',', '')
            # _area_SQWs = _area.split('ไร่')[1].split('งาน')[1].split('ตารางวา')[0]
            pattern = r'(\d+(?:\.\d+)?)\sตารางวา'
            matches = re.findall(pattern, _area)  # Find all matches in the data
            # print(_area)
            # Print the extracted numbers
            for _area_SQWs in matches:
                # print(match)
                # _area_rai = _area.split('ตารางวา')

                print(_area_SQWs)
            # print(_area)
            # print(_area_SQWs)
            area_SQWs.append(_area_SQWs)

        except Exception as err:
            area_SQWs.append('0')


        try:
            room = soup.find(text="จำนวนห้อง : ").parent.parent.get_text().strip().split('\n')[0]
            # print(room)
        except Exception as err:
            room = 'none'

        try:
            _bedrooms = room.split(' ')[0]
            if _bedrooms == 'ห้องสตูดิโอ':
                _bedrooms = 'none'
            bedrooms.append(_bedrooms)
        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms = room.split(' ')[2]
            if _bathrooms == 'ห้องน้ำ':
                _bathrooms = room.split(' ')[1]
            bathrooms.append(_bathrooms)
        except Exception as err:
            bathrooms.append('none')

        try:
            _garages = room.split(' ')[5]
            if _garages == 'คัน':
                _garages = room.split(' ')[4]
            garages.append(_garages)
        except Exception as err:
            garages.append('none')

        try:
            _detail = soup.find('div', class_='headtitle2').get_text().replace('\n', ' ').replace('\r', '').replace(',', '')
            details.append(_detail)
        except Exception as err:
            details.append('none')

        try:
            _house_pictures = soup.find('div', {'id': 'divImg'}).find('img', {'class': 'images_show'})['src']
            house_pictures.append("https://www.prakardproperty.com" + _house_pictures)
            # print(house_pictures)
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
            _seller_names = soup.find('span', {'id': 'rName'}).get_text().strip().replace(',', '')
            seller_names.append(_seller_names)
        except Exception as err:
            seller_names.append('none')

        try:
            _seller_tels = soup.find('div', {'id': 'PhoneMember'}).get_text().strip().replace(',', '')
            print(_seller_tels)
            seller_tels.append(_seller_tels)
            print(seller_tels)
        except Exception as err:
            seller_tels.append('none')
            print('\n', prop_url)
            print('ERROR!!! =>', err)

        print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)
        # seller_tels.append('none')
        print('\n', prop_url)
        print('ERROR!!! =>', err)
        house_pictures.append('none')
        area.append('none')
        area_rai.append('none')
        area_Ngan.append('none')
        area_SQWs.append('none')
        source_ids.append('none')
        bedrooms.append('none')
        bathrooms.append('none')
        garages.append('none')
        details.append('none')
        days.append('none')
        months.append('none')
        years.append('none')
        post_dates.append('none')
        seller_names.append('none')
        seller_tels.append('none')


if __name__ == "__main__":
    # GET LINK
    for prop_type in property_type:
        save_list_links(prop_type)


    # GET DATA
    for prop_type in property_type:
        print("---------------------::  GET DATA " + prop_type + "  ::---------------------")
        loop_links(prop_type)
        sleep(0.5)
    #
    print('ids', len(ids))
    print('ref_code',len(ref_code))
    print('webs', len(webs))
    print('names', len(names))
    print('house_pictures', len(house_pictures))
    print('project_names', len(project_names))
    print('addresss', len(addresss))
    print('province ', len(province))
    print('district ', len(district))
    print('sub_district ', len(sub_district))
    print('province_codes', len(province_codes))
    print('district_codes', len(district_codes))
    print('sub_district_codes', len(sub_district_codes))
    print('prices', len(prices))
    print('range_of_house_prices', len(range_of_house_prices))
    print('area', len(area))
    print('area_rai', len(area_rai))
    print('area_Ngan', len(area_Ngan))
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


    # def fill_list(lst, target_length, fill_value=None):
    #     return lst + [fill_value] * (target_length - len(lst))
    #
    #     # Get the length of the longest list
    #
    #
    # max_length = max(
    #     len(ids), len(ref_code), len(webs), len(names), len(house_pictures),
    #     len(project_names), len(addresss), len(province), len(district),
    #     len(sub_district), len(sub_district_codes), len(district_codes), len(province_codes),
    #     len(prices), len(range_of_house_prices), len(area), len(area_rai), len(area_Ngan),
    #     len(area_SQWs), len(floor_numbers), len(floors), len(room_numbers), len(bedrooms),
    #     len(bathrooms), len(garages), len(latitudes), len(longtitudes), len(details),
    #     len(seller_names), len(seller_tels), len(seller_emails), len(seller_ids),
    #     len(house_links), len(type_ids), len(sell_type_ids), len(source_ids), len(duplicates),
    #     len(news), len(cross_webs), len(cross_refs), len(completion_years), len(years),
    #     len(months), len(days), len(post_dates), len(date_times)
    # )
    #
    # # Fill all lists to match the maximum length
    # ids = fill_list(ids, max_length)
    # ref_code = fill_list(ref_code, max_length)
    # webs = fill_list(webs, max_length)
    # names = fill_list(names, max_length)
    # house_pictures = fill_list(house_pictures, max_length)
    # project_names = fill_list(project_names, max_length)
    # addresss = fill_list(addresss, max_length)
    # province = fill_list(province, max_length)
    # district = fill_list(district, max_length)
    # sub_district = fill_list(sub_district, max_length)
    # sub_district_codes = fill_list(sub_district_codes, max_length)
    # district_codes = fill_list(district_codes, max_length)
    # province_codes = fill_list(province_codes, max_length)
    # prices = fill_list(prices, max_length)
    # range_of_house_prices = fill_list(range_of_house_prices, max_length)
    # area = fill_list(area, max_length)
    # area_rai = fill_list(area_rai, max_length)
    # area_Ngan = fill_list(area_Ngan, max_length)
    # area_SQWs = fill_list(area_SQWs, max_length)
    # floor_numbers = fill_list(floor_numbers, max_length)
    # floors = fill_list(floors, max_length)
    # room_numbers = fill_list(room_numbers, max_length)
    # bedrooms = fill_list(bedrooms, max_length)
    # bathrooms = fill_list(bathrooms, max_length)
    # garages = fill_list(garages, max_length)
    # latitudes = fill_list(latitudes, max_length)
    # longtitudes = fill_list(longtitudes, max_length)
    # details = fill_list(details, max_length)
    # seller_names = fill_list(seller_names, max_length)
    # seller_tels = fill_list(seller_tels, max_length)
    # seller_emails = fill_list(seller_emails, max_length)
    # seller_ids = fill_list(seller_ids, max_length)
    # house_links = fill_list(house_links, max_length)
    # type_ids = fill_list(type_ids, max_length)
    # sell_type_ids = fill_list(sell_type_ids, max_length)
    # source_ids = fill_list(source_ids, max_length)
    # duplicates = fill_list(duplicates, max_length)
    # news = fill_list(news, max_length)
    # cross_webs = fill_list(cross_webs, max_length)
    # cross_refs = fill_list(cross_refs, max_length)
    # completion_years = fill_list(completion_years, max_length)
    # years = fill_list(years, max_length)
    # months = fill_list(months, max_length)
    # days = fill_list(days, max_length)
    # post_dates = fill_list(post_dates, max_length)
    # date_times = fill_list(date_times, max_length)

    # Create DataFrame and save to CSV
    property_list = pd.DataFrame({
        'ID': ids,
        'ref_code': ref_code,
        'web': webs,
        'name': names,
        'project_name': project_names,
        'address': addresss,
        'province': province,
        'district': district,
        'sub_district': sub_district,
        'subdistrict_code': sub_district_codes,
        'district_code': district_codes,
        'province_code': province_codes,
        'price': prices,
        'range_of_house_price': range_of_house_prices,
        'area': area,
        'area_rai': area_rai,
        'area_Ngan': area_Ngan,
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
        'duplicate': duplicates,
        'new': news,
        'cross_web': cross_webs,
        'cross_ref': cross_refs,
        'completion_year': completion_years,
        'year': years,
        'month': months,
        'day': days,
        'post_date': post_dates,
        'date_time': date_times,
        'update_date': post_dates,
    })

    property_list.to_csv(path_Files + '/' + web + '.csv', index=False)
    print('Export', len(ids), 'Rows To CSV File Completed!!!!')