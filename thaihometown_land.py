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

# base_url = "https://www.thaihometown.com/search/?page=placeholder_page&FormType=Sale&Type=placeholder_type&Submit=Search"
base_url ="https://www.thaihometown.com/search/?page=placeholder_page&FormType=Sale&Type=placeholder_type&Submit=Search"


# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'thaihometownland'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 6, 20).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

property_type = {
    # "Land": {"type_id": 1, "route": "Land", "r_type": "land", "start": 368 ,"end": 490} 
    "Land": {"type_id": 1, "route": "Land", "r_type": "land", "start": 1 ,"end": 23} 
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

# ---- Path ----
path_links = os.path.join("links", date, web)
path_files = os.path.join("Files", date, web)

# ---- Create directories if they don't exist ----
os.makedirs(path_links, exist_ok=True)
os.makedirs(path_files, exist_ok=True)

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

def reset_list():
    # เพิ่ม global สำหรับตัวแปรลิสต์ทั้งหมด
    global ids
    global ref_code
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
    ref_code = []
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
            _ref_code = soup.find('div', class_ ='NoID').get_text().strip().replace("\n","").replace("No.","").replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            print(_ref_code)
            ref_code.append(_ref_code)
        except Exception as err:
            ref_code.append('none')

        try:
            name = soup.find('title').get_text().split('|')[0].strip().replace(',', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(name)
            names.append(name)
        except Exception as err:
            names.append('none')

        try:
            _latitude = soup.find('div', class_='maps_google2').parent.iframe['src'].split('!3d')[1].split('!')[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            latitudes.append(_latitude)
            print(_latitude)
        except Exception as err:
            latitudes.append('none')


        try:
            _longtitudes = soup.find('div', class_='maps_google2').parent.iframe['src'].split('!2d')[1].split('!')[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            longtitudes.append(_longtitudes)
            print(_longtitudes)
        except Exception as err:
            longtitudes.append('none')

        try:
            # _province = soup.find(text="จังหวัดที่ตั้ง : ").parent.parent.get_text().strip().split("\n")[2]
            _provinces = soup.find_all('a', class_='linkcity')[1].get_text().strip().replace('ตารางวา', '').replace('ตารางเมตร', '').replace('  ', '').replace(',', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            _provinces = re.sub(r'\d+', ' ', _provinces)
            province.append(_provinces)

            # print(_provinces)
        except Exception as err:
            province.append('none')

        try:
            _district = soup.find_all('a', class_='linkcity')[2].get_text().strip().replace('ตารางวา', '').replace('ตารางเมตร', '').replace('  ', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            _district = re.sub(r'\d+', ' ', _district)
            district.append(_district)
        except Exception as err:
            district.append('none')

        try:
            _sub_district = soup.find_all('a', class_='linkcity')[3].get_text().strip().replace('ตารางวา', '').replace('ตารางเมตร', '').replace('  ', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
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
                _prices = int(re.sub('[^0-9]', '', _price[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()))
                prices.append(_prices)
            else:
                _prices = int(re.sub('[^0-9]', '', _price[2].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()))
                prices.append(_prices)


            range_of_house_prices.append(fn.get_range_of_price(_prices))
        except Exception as err:
            prices.append(0)
            range_of_house_prices.append(9)


        try:
            _area = soup.find('div', class_='sqm_right').parent.parent.get_text().strip().replace('เนื้อที่รวม : ', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            if _area == '':
                _area = \
                soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split(
                    "ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('', '').replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(_area)
            area.append(_area)
        except AttributeError:
            _area = \
            soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split(
                "ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('', '').replace('\n', '').replace('\t', '').replace(
                'ขนาดที่ดิน', '').replace('\r', '').replace(',','').replace('\n', ' ').replace('\t', ' ').strip()
            print(_area)
            area.append(_area)
        except Exception as err:
            area.append('none')

        try:
            _area = soup.find('td', class_='table_set3').parent.parent.get_text().strip().split("เนื้อที่รวม :")[1].split("ราคา :")[0].split("พื้นที่ใช้สอย :")[0].replace('','') \
                .replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
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
                .replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
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
                .replace('\n', '').replace('\t', '').replace('ขนาดที่ดิน', '').replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
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
            room = soup.find(text="จำนวนห้อง : ").parent.parent.get_text().strip().split('\n')[0].replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            # print(room)
        except Exception as err:
            room = 'none'

        try:
            _bedrooms = room.split(' ')[0]
            if _bedrooms == 'ห้องสตูดิโอ':
                _bedrooms = 'none'
            bedrooms.append(_bedrooms.replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())
        except Exception as err:
            bedrooms.append('none')

        try:
            _bathrooms = room.split(' ')[2]
            if _bathrooms == 'ห้องน้ำ':
                _bathrooms = room.split(' ')[1]
            bathrooms.append(_bathrooms.replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())
        except Exception as err:
            bathrooms.append('none')

        try:
            _garages = room.split(' ')[5]
            if _garages == 'คัน':
                _garages = room.split(' ')[4]
            garages.append(_garages.replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip())
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
            _seller_names = soup.find('span', {'id': 'rName'}).get_text().strip().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            seller_names.append(_seller_names)
        except Exception as err:
            seller_names.append('none')

        try:
            _seller_tels = soup.find('div', {'id': 'PhoneMember'}).get_text().strip().replace(',','').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            print(_seller_tels)
            seller_tels.append(_seller_tels)
            print(seller_tels)
        except Exception as err:
            seller_tels.append('none')
            print('\n', prop_url)
            print('ERROR!!! =>', err)

        # print('Get Data OK')
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
                print('ref_code', len(ref_code))
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
                    'ref_code': ref_code,
                    'web': webs,
                    'name': names,
                    'project_name': project_names,
                    'address': addresss,
                    'subdistrict_code': sub_district_codes,
                    'district_code': district_codes,
                    'province_code': province_codes,
                    'price': prices,
                    'range_of_house_price': range_of_house_prices,
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