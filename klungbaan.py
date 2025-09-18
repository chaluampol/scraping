import requests
# import lib_helper as hp
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import codecs
import os
from tqdm import tqdm
from fake_useragent import UserAgent
import reic_function as fn
from time import sleep



## url แบบเก่า
# base_url = "https://placeholder_link_web.klungbaan.com/search-result/page/placeholder_page/?status=placeholder_list_type&keyword=&states=&type=placeholder_type&bedrooms=&bathrooms=&min-price=&max-price=&sortby=d_date"

base_url = "https://placeholder_link_web.klungbaan.com/search-result/page/placeholder_page/?status=placeholder_list_type&keyword&states&type=placeholder_type&bedrooms&bathrooms&min-price&max-price&sortby=d_date%22"
ua = UserAgent()

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'klungbaan'
get_types = ['LINK', 'DATA'] #'LINK', 'DATA'
# date = datetime(2025, 9, 8).strftime('%Y-%m-%d') # manual
date = datetime.today().strftime('%Y-%m-%d') # auto
date_now = fn.get_date_now()

# +++++++++++++ ประเภททรัพย์ +++++++++++++ #
property_type = {
    "home": {"type_id": 1, "route": "single-house", "link_web": "www", "list_type": "sale", "start": 1, "end": 27},
    "condo": {"type_id": 2, "route": "condo", "link_web": "www", "list_type": "sale", "start": 1, "end": 16},
    "townhouse": {"type_id": 3, "route": "townhome", "link_web": "www", "list_type": "sale", "start": 1, "end": 24},
    # # #
    "home_rent": {"type_id": 1, "route": "single-house", "link_web": "rent", "list_type": "rent", "start": 1, "end": 5},
    "condo_rent": {"type_id": 2, "route": "condo", "link_web": "rent", "list_type": "rent", "start": 1, "end": 7},
    "townhouse_rent": {"type_id": 3, "route": "townhome", "link_web": "rent", "list_type": "rent", "start": 1, "end": 4}

}
thai_full_months = [
    "มกราคม",
    "กุมภาพันธ์",
    "มีนาคม",
    "เมษายน",
    "พฤษภาคม",
    "มิถุนายน",
    "กรกฎาคม",
    "สิงหาคม",
    "กันยายน",
    "ตุลาคม",
    "พฤศจิกายน",
    "ธันวาคม",
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
completion_years = []
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


def get_data(prop_url, type_id):
    user_agent = ua.random
    Headers = {'User-Agent': user_agent}
    req = requests.get(prop_url, headers=Headers)
    req.encoding = "utf-8"
    soup = BeautifulSoup(req.text, 'html.parser')

    try:
        _o = int(0)
        try:
            name = soup.find("title").get_text().split(" - ")[0].strip()
            names.append(name)
        except Exception as err:
            names.append("none")

        try:
            house_picture = soup.find('div', id="property-gallery-js").find('img', class_='img-fluid')['src']
            house_pictures.append(house_picture)
        except Exception as err:
            house_pictures.append("none")

        try:
            _project_name = soup.find('li', class_='project_name')
            if _project_name != None:
                project_name = _project_name.find('span').get_text()
                project_names.append(project_name)
            else:
                project_names.append('none')
        except Exception as err:
            project_names.append('none')

        try:
            address = soup.find('div', id='property-address-wrap').find('li',
                                                                        class_='detail-address').get_text().strip()
            addresss.append(address)
        except Exception as err:
            addresss.append('none')

        try:
            try:
                _province = soup.find('li', class_='detail-state').a.get_text().strip()
            except Exception as err:
                _province = 'none'

            try:
                _district = soup.find('li', class_='detail-city').a.get_text().replace('เขต', '').strip()
            except Exception as err:
                _district = 'none'

            try:
                _subdistrict = \
                    soup.find('li', class_='detail-area').a.get_text().replace('โซน', '').split(' ')[0].split('-')[
                        0].strip()
            except Exception as err:
                _subdistrict = 'none'

            province_code, district_code, sub_district_code = fn.prov_dis_subdis(_province, _district, _subdistrict)

            province_codes.append(int(province_code))
            district_codes.append(int(district_code))
            sub_district_codes.append(int(sub_district_code))
        except:
            province_codes.append('none')
            district_codes.append('none')
            sub_district_codes.append('none')

        try:
            price = soup.find('div', class_='page-title-wrap').find('li', class_='item-price').get_text().replace(',',
                                                                                                                  '').split(
                ' ')[0].strip()
            prices.append(price)
            range_of_house_prices.append(fn.get_range_of_price(int(price)))
        except Exception as err:
            prices.append(_o)
            range_of_house_prices.append(9)

        try:
            area_SQM = soup.find('li', class_='prop_size').span.get_text().split(" ")[0].strip()
            if area_SQM == '-':
                area_SQM = 'none'
            else:
                area_SQM = str(float(area_SQM))
            area_SQMs.append(area_SQM)
        except Exception as err:
            area_SQMs.append('none')

        try:
            area_SQW = soup.find('li', class_='property_area_rai').span.get_text().strip()
            if area_SQW == '-':
                area_SQW = 'none'
            area_SQWs.append(area_SQW)
        except Exception as err:
            area_SQWs.append('none')

        try:
            floor_number = soup.find('li', class_='amount_floor').span.get_text().replace('ชั้น', '').strip()
            if floor_number == '-':
                floor_number = 'none'
            floor_numbers.append(floor_number)
        except Exception as err:
            floor_numbers.append('none')

        try:
            floor = soup.find_all('li', class_='building_name')[1].span.get_text()
            if floor == '-':
                floor = 'none'
            floors.append(floor)
        except Exception as err:
            floors.append('none')



        try:
            bedroom = soup.find('li', class_='bedrooms').span.get_text().replace('ห้อง', '').strip()
            bedrooms.append(int(bedroom))
        except Exception as err:
            bedrooms.append(0)

        try:
            bathroom = soup.find('li', class_='bathrooms').span.get_text().replace('ห้อง', '').strip()
            bathrooms.append(int(bathroom))
        except Exception as err:
            bathrooms.append(0)

        try:
            garage = soup.find('li', class_='garage').span.get_text().replace('คัน', '').strip()
            garages.append(int(garage))
        except Exception as err:
            garages.append(0)

        try:
            _detail = soup.find('div', id='property-description-wrap').find_all('p')
            detail = ''
            for i in _detail:
                detail += i.get_text().replace(',', ' ').replace('\n', ' ').replace('\r', ' ')
            details.append(detail)
        except Exception as err:
            details.append('none')

        try:
            _location = soup.find('a', id='pills-street-view-tab')['href'].split('&')
            for i in _location:
                if not str(i).find('cbll'):
                    latitude = i.replace('cbll=', '').split(',')[0].strip()
                    longtitude = i.replace('cbll=', '').split(',')[1].strip()
            latitudes.append(latitude)
            longtitudes.append(longtitude)
        except Exception as err:
            latitudes.append('none')
            longtitudes.append('none')


        try:
            _update_date = soup.find('span', class_='small-text grey').get_text().strip().split(' ')
            day = _update_date[2].replace(',', '')
            month = thai_full_months.index(_update_date[1]) + 1
            year = _update_date[3]
            days.append(int(day))
            months.append(int(month))
            years.append(int(year))
            post_dates.append(str(year) + '-' + str(month) + '-' + str(day))
        except Exception as err:
            days.append('none')
            months.append('none')
            years.append('none')
            post_dates.append('none')

        try:
            seller_name = soup.find('ul', class_='agent-information list-unstyled').find('li',
                                                                                         class_='agent-name').get_text()
            seller_names.append(seller_name)
        except Exception as err:
            seller_names.append('none')

        try:
            seller_tel = soup.find('li', class_='detail-tel').a.get_text().strip()
            seller_tels.append(seller_tel)
        except Exception as err:
            seller_tels.append('none')

        try:
            _contact_info = soup.find('div', class_='property-address-wrap property-section-wrap')
            seller_email = _contact_info.find_all('li', class_='detail-address')[1].span.get_text()
            seller_emails.append(seller_email)
        except Exception as err:
            seller_emails.append('none')

        try:
            if property_type[prop_type]["property_sell_rent"] == "sale":
                _sell_type_ids = int(1)
            else:
                _sell_type_ids = int(2)
            sell_type_ids.append(_sell_type_ids)
        except Exception as err:
            sell_type_ids.append(int(1))

        seller_ids.append(_o)
        room_numbers.append(_o)
        house_links.append(prop_url)
        completion_years.append('none')
        date_times.append(date_now)
        type_ids.append(int(type_id))
        duplicates.append(_o)
        news.append(int(1))
        cross_webs.append('none')
        cross_refs.append('none')
        source_ids.append(int(fn.get_source_id(web)))
        webs.append(web)

        # print('Get Data OK')
    except Exception as err:
        print('\n', prop_url)
        print('ERROR!!! =>', err)


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

def save_list_links(prop_type):
    print("---------------------::  GET LINK " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    route = property_type[prop_type]["route"]
    link_web = property_type[prop_type]["link_web"]
    list_type = property_type[prop_type]["list_type"]
    req_url = base_url.replace("placeholder_type", route).replace("placeholder_link_web", str(link_web)).replace("placeholder_list_type", str(list_type))
    # for (s, r) in (type_sell, type_rent):
    #     print("------------------:: ", s, " ::---------------------------")
    for i in tqdm(range(start_page, end_page)):
        Headers = {'User-Agent': ua.random}
        wait_time = 0.25
        url = req_url.replace("placeholder_page", str(i))
        req = requests.get(url, headers=Headers)
        while req.status_code != 200:
            req = requests.get(url, headers=Headers)

        soup = BeautifulSoup(req.text, "html.parser")
        _item = soup.find_all('h2', class_='item-title')
        if len(_item) > 0:
            file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
            for j in _item:
                _link = j.a['href']
                file_links.writelines(_link + "\n")
            file_links.close()
            sleep(wait_time)


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

            # upload files to google drive.
            fn.upload_processing(date, web)

