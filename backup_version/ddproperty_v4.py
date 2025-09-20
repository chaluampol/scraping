import os
import random
import time
import json
import ssl
import reic_function as fn
import logging
import codecs
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #
web = 'ddproperty'
get_types = ['DATA'] #'LINK', 'DATA'
date = datetime(2025, 5, 27).strftime('%Y-%m-%d')

property_type = {
    'home'          : {'type_id': 1, 'type_value': 'B', 'route': 'BUNG', "property_sell_rent": 'รวมประกาศขาย', 'listing_type': 'sell', 'start': 1, 'end': 50},
    'condo'         : {'type_id': 2, 'type_value': 'N', 'route': 'CONDO', "property_sell_rent": 'รวมประกาศขาย', 'listing_type': 'sell', 'start': 1, 'end': 75},
    'townhouse'     : {'type_id': 3, 'type_value': 'T', 'route': 'TOWN', "property_sell_rent": 'รวมประกาศขาย', 'listing_type': 'sell', 'start': 1, 'end': 25},
    'home_rent'     : {'type_id': 1, 'type_value': 'B', 'route': 'BUNG', "property_sell_rent": 'รวมประกาศให้เช่า', 'listing_type': 'rent', 'start': 1, 'end': 30},
    'condo_rent'    : {'type_id': 2, 'type_value': 'N', 'route': 'CONDO', "property_sell_rent": 'รวมประกาศให้เช่า', 'listing_type': 'rent', 'start': 1, 'end': 50},
    'townhouse_rent': {'type_id': 3, 'type_value': 'T', 'route': 'TOWN', "property_sell_rent": 'รวมประกาศให้เช่า', 'listing_type': 'rent', 'start': 1, 'end': 20},
}
# +++++++++++++ แก้ข้อมูลเพื่อเก็บข้อมูล +++++++++++++ #



date_now = fn.get_date_now()
_day = date_now.split("-")[2]
_month = date_now.split("-")[1]
_year = date_now.split("-")[0]


thai_months_abbr = [
    "ม.ค.",  # มกราคม
    "ก.พ.",  # กุมภาพันธ์
    "มี.ค.",  # มีนาคม
    "เม.ย.",  # เมษายน
    "พ.ค.",  # พฤษภาคม
    "มิ.ย.",  # มิถุนายน
    "ก.ค.",  # กรกฎาคม
    "ส.ค.",  # สิงหาคม
    "ก.ย.",  # กันยายน
    "ต.ค.",  # ตุลาคม
    "พ.ย.",  # พฤศจิกายน
    "ธ.ค."   # ธันวาคม
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

logging.getLogger("playwright").setLevel(logging.CRITICAL)
ua = UserAgent()

VIEWPORTS = [
    {"width": 1920, "height": 1080},   # Desktop
    {"width": 1600, "height": 900},    # Laptop
    {"width": 1366, "height": 768},    # Tablet
    {"width": 375, "height": 667}      # iPhone 8
]

LOCALE_TIMEZONE_PAIRS = [
    ("en-US", "America/New_York"),
    ("en-GB", "Europe/London"),
    ("th-TH", "Asia/Bangkok"),
    ("ja-JP", "Asia/Tokyo"),
    ("ko-KR", "Asia/Seoul"),
    ("zh-CN", "Asia/Shanghai"),
    ("fr-FR", "Europe/Paris"),
    ("de-DE", "Europe/Berlin"),
    ("es-ES", "Europe/Madrid"),
    ("pt-BR", "America/Sao_Paulo")
]

REFERERS = [
    "https://www.google.com/",
    "https://www.bing.com/",
    "https://www.facebook.com/",
    "https://twitter.com/",
    "https://www.reddit.com/",
    "https://www.ddproperty.com/"
]

def reset_list():
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

# ---- ฟังก์ชันจำลอง delay แบบมนุษย์ ----
def human_wait(min_ms=100, max_ms=300):
    time.sleep(random.uniform(min_ms / 1000, max_ms / 1500))

def captcha_detect(content):
    return ('<meta content="noindex,nofollow" name="robots"/>' in content.lower()
            or 'id="captcha_login"' in content.lower()
            or "we just want to make sure you are a human" in content.lower()
            or "just a moment..." in content.lower()
            or "verify you are human by completing the action below." in content.lower()
            )

def get_page_content(url: str = ""):
    if url == "":
        return "url_not_found"

    # ---- เริ่มใช้งาน Playwright ----
    with sync_playwright() as p:
        # สุ่มค่าจำลอง
        user_agent = ua.random
        viewport = random.choice(VIEWPORTS)
        locale, timezone = random.choice(LOCALE_TIMEZONE_PAIRS)
        referer = random.choice(REFERERS)
        base_device = dict(random.choice([p.devices["iPhone 8"], p.devices["Pixel 5"]]))

        # แก้ไข device ให้ใช้ค่าที่เรากำหนด
        base_device["user_agent"] = user_agent
        base_device["locale"] = locale
        base_device["timezone_id"] = timezone
        base_device["viewport"] = viewport

        browser = p.chromium.launch(
            headless=True,
            executable_path=fn.get_browser_path()
        )

        context = browser.new_context(**base_device)
        context.set_default_navigation_timeout(90000)

        page = context.new_page()

        # ตั้งค่า HTTP headers เพิ่มเติม
        page.set_extra_http_headers({
            "Accept-Language": f"{locale},en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1",
            "Referer": referer
        })

        page.goto(url=url, wait_until="domcontentloaded", timeout=60000)

        # # Scroll และ mouse move แบบสุ่ม
        # page.mouse.wheel(0, random.randint(100, 1000))
        # # human_wait()
        # page.mouse.move(random.randint(0, viewport["width"]), random.randint(0, viewport["height"]))
        # # human_wait()
        #
        # # พิมพ์ข้อความในช่องค้นหา (หากเจอ)
        # try:
        #     search_input = page.query_selector("input[type='search'], input[type='text']")
        #     if search_input:
        #         search_input.click()
        #         # human_wait()
        #         search_input.type("บ้านให้เช่า", delay=random.randint(10, 20))
        #         # human_wait()
        # except Exception as e:
        #     print("❗ ข้ามการพิมพ์:", e)
        #
        # # คลิกลิงก์แบบสุ่ม (จำลองพฤติกรรมคลิก)
        # try:
        #     links = page.query_selector_all("a")
        #     if links:
        #         random.choice(links).click()
        #         # human_wait()
        # except Exception as e:
        #     print("❗ ข้ามการคลิก:", e)


        soup = BeautifulSoup(page.content(), "html.parser")
        next_data_script = soup.find("script", {"id": "__NEXT_DATA__"})

        # browser.close()
        # time.sleep(random.uniform(1.5, 3))
        if next_data_script:
            return next_data_script
        else:
            return "content_not_found"

def save_list_links(prop_type):
    print("---------------------::  GET LINK " + prop_type + "  ::---------------------")
    start_page = property_type[prop_type]["start"]
    end_page = property_type[prop_type]["end"] + 1
    type_value = property_type[prop_type]["type_value"]
    route = property_type[prop_type]["route"]
    list_type = property_type[prop_type]["property_sell_rent"]
    listing_type = property_type[prop_type]["listing_type"]

    for i in tqdm(range(int(start_page), int(end_page))):
        # url = f'https://www.ddproperty.com/{list_type}?page={i}&listingType={listing_type}&propertyTypeGroup={route}&sort=date&order=desc'
        url = f"https://www.ddproperty.com/{list_type}?page={i}&listingType={listing_type}&propertyTypeGroup={type_value}&propertyTypeCode={route}&isCommercial=false&sort=date&order=desc"

        next_data_script = get_page_content(url)
        while next_data_script == "content_not_found":
            next_data_script = get_page_content(url)

        if next_data_script != "content_not_found":
            next_data_json = json.loads(next_data_script.string)

            data_json = next_data_json['props']
            pageProps = data_json['pageProps']
            pageData = pageProps['pageData']
            pageData_data = pageData['data']
            listingsData = pageData_data['listingsData']

            file_links = codecs.open(path_links + f"/links_{prop_type}.txt", "a+", "utf-8")
            for _data in listingsData:
                _link = _data['listingData']['url']
                # print('_link', _link)
                file_links.writelines(_link + "\n")
            file_links.close()
        # break

def get_detail(prop_url: str, type_id: int, ID: int):
    if prop_url:
        next_data_script = get_page_content(prop_url)
        # print('next_data_script', next_data_script)
        if next_data_script != "content_not_found":
            try:
                # แปลง JSON ข้างใน script tag
                next_data_json = json.loads(next_data_script.string)

                # print(next_data_json)
                data_json = next_data_json['props']
                pageProps = data_json['pageProps']
                pageData = pageProps['pageData']
                pageData_data = pageData['data']
                try:
                    metatable = pageData_data['detailsData']['metatable']['items']
                except:
                    metatable = pageData_data['projectListingData']['metatable']['items']

                ids.append(ID)
                webs.append(web)
                # house_links.append(prop_url)
                # type_ids.append(type_id)
                garages.append('none')
                duplicates.append(0)
                news.append(int(1))
                cross_webs.append('none')
                cross_refs.append('none')
                room_numbers.append('none')
                seller_ids.append(0)
                floors.append('none')


                try:
                    _name = pageData_data['metadata']['metaTags']['title']
                    names.append(_name)
                except Exception as err:
                    names.append('none')

                try:
                    _project_name = pageData_data['listingData']['localizedTitle']
                    if _project_name == 'ไม่มีข้อมูล':
                        _project_name = 'none'
                    project_names.append(_project_name)
                except Exception as error:
                    project_names.append('none')

                try:
                    # print('addresss1 =>', pageData_data['propertyOverviewData']['locationInfo']['fullAddress'].strip().replace(',', ''))
                    _address = pageData_data['propertyOverviewData']['locationInfo']['fullAddress'].strip().replace(',', '')
                    _addresss = _address.split(' ')
                    _subdistrict = _addresss[len(_addresss) - 3]
                    _district = _addresss[len(_addresss) - 2]
                    _province = _addresss[len(_addresss) - 1]

                    _prrovince_code, _district_code, _subdistrict_code = fn.prov_dis_subdis(_province, _district, _subdistrict)

                    addresss.append(_address)
                    province_codes.append(_prrovince_code)
                    district_codes.append(_district_code)
                    sub_district_codes.append(_subdistrict_code)
                except:
                    try:
                        # print('addresss2 =>', pageData_data['propertyOverviewData']['propertyInfo']['fullAddress'])
                        _address = pageData_data['propertyOverviewData']['propertyInfo']['fullAddress'].strip().replace(',', '')
                        _addresss = _address.split(' ')
                        _subdistrict = _addresss[len(_addresss) - 3]
                        _district = _addresss[len(_addresss) - 2]
                        _province = _addresss[len(_addresss) - 1]

                        _prrovince_code, _district_code, _subdistrict_code = fn.prov_dis_subdis(_province, _district, _subdistrict)

                        addresss.append(_address)
                        province_codes.append(_prrovince_code)
                        district_codes.append(_district_code)
                        sub_district_codes.append(_subdistrict_code)
                    except:
                        addresss.append(0)
                        province_codes.append(0)
                        district_codes.append(0)
                        sub_district_codes.append(0)

                try:
                    # print('price =>', pageData_data['listingData']['priceValue'])
                    _price = pageData_data['listingData']['priceValue']
                    prices.append(_price)
                    range_of_house_prices.append(fn.get_range_of_price(_price))
                except:
                    try:
                        # print('price =>', pageData_data['listingData']['price'])
                        _price = pageData_data['listingData']['price']
                        prices.append(_price)
                        range_of_house_prices.append(fn.get_range_of_price(_price))
                    except:
                        prices.append(0)
                        range_of_house_prices.append(9)

                # print('listingData', pageData_data['listingData'])

                try:
                    if type_id == 1 or type_id == 3:
                        # print('area_SQW', pageData_data['listingData']['landArea'])
                        _area_SQWs = pageData_data['listingData']['landArea']
                        area_SQWs.append(_area_SQWs)
                        area_SQMs.append('none')
                    else:
                        # print('area_SQM', pageData_data['listingData']['floorArea'])
                        _area_SQMs = pageData_data['listingData']['floorArea']
                        area_SQMs.append(_area_SQMs)
                        area_SQWs.append('none')
                except:
                    area_SQWs.append('none')
                    area_SQMs.append('none')


                try:
                    _listingTypeText = pageData_data['listingData']
                    _sell_type_id = fn.get_sell_typeID(_listingTypeText)
                    sell_type_ids.append(_sell_type_id)
                except:
                    sell_type_ids.append(1)

                try:
                    _bed_room = pageData_data['listingData']['bedrooms']
                    bedrooms.append(_bed_room)
                except:
                    bedrooms.append('none')

                try:
                    _bath_room = pageData_data['listingData']['bathrooms']
                    bathrooms.append(_bath_room)
                except:
                    bathrooms.append('none')

                try:
                    # print('detail =>', pageData_data['metadata']['metaTags']['openGraph']['description'])
                    _detail = pageData_data['metadata']['metaTags']['openGraph']['description']\
                                            .replace('\n', ' ')\
                                            .replace('\r', ' ')\
                                            .replace('\t', ' ')\
                                            .replace("'", '')\
                                            .replace('                     ', ' ')
                    details.append(_detail)
                except:
                    details.append('none')


                try:
                    _lat = pageData_data['listingLocationData']['data']['center']['lat']
                    _lng = pageData_data['listingLocationData']['data']['center']['lng']
                    latitudes.append(_lat)
                    longtitudes.append(_lng)
                except:
                    latitudes.append('none')
                    longtitudes.append('none')

                try:
                    _floor_number = next((item for item in metatable if item["icon"] == 'layers-2-o'), None)
                    if type_id == 2:
                        floor_numbers.append(_floor_number['value'].split(' ')[1])
                    else:
                        floor_numbers.append('none')
                except:
                    floor_numbers.append('none')

                try:
                    _house_piture = pageData_data['metadata']['metaTags']['openGraph']['image']
                    house_pictures.append(_house_piture)
                except Exception as err:
                    house_pictures.append('none')

                try:
                    source_ids.append(int(fn.get_source_id(web)))
                except Exception as err:
                    source_ids.append(0)

                house_links.append(prop_url)
                type_ids.append(type_id)


                try:
                    _seller = pageData_data['listingData']['agent']
                    _seller_name = _seller['name']
                    _seller_email = _seller['email']
                    _seller_tel = _seller['name'].replace('+66', '0')
                    seller_names.append(_seller_name)
                    seller_emails.append(_seller_email)
                    seller_tels.append(_seller_tel)
                except:
                    seller_names.append('none')
                    seller_emails.append('none')
                    seller_tels.append('none')

                try:
                    _completion_year = next((item for item in metatable if item["icon"] == 'document-with-lines-o'), None)
                    completion_years.append(int(_completion_year['value'].split(' ')[1]) - 543)
                except:
                    completion_years.append('none')


                try:
                    _post_date = next((item for item in metatable if item["icon"] == 'calendar-time-o'), None)
                    _post_date_arr = _post_date['value'].split(' ')

                    days.append(int(_post_date_arr[1]))
                    months.append(int(thai_months_abbr.index(_post_date_arr[2])) + 1)
                    years.append(int(_post_date_arr[3]))
                    post_dates.append(datetime(int(_post_date_arr[3]), int(thai_months_abbr.index(_post_date_arr[2])) + 1, int(_post_date_arr[1])))
                except:
                    days.append('none')
                    months.append('none')
                    years.append('none')
                    post_dates.append('none')

                date_times.append(date_now)

            except Exception as e:
                print("⚠️ ไม่สามารถแปลง JSON ได้:", e)
        else:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "❌ ไม่พบ <script id='__NEXT_DATA__'>")
            get_detail(prop_url, type_id, ID)
    else:
        print('url_not_found')

def loop_links(prop_type, ID=0):
    file_links = codecs.open(path_links + f'/links_{prop_type}.txt', 'r', 'utf-8')
    links = file_links.readlines()
    file_links.close()

    type_id = property_type[prop_type]['type_id']
    for j in tqdm(range(len(links))):
        ID += 1
        link = links[j]
        try:
            get_detail(link.strip(), type_id, ID)
        except Exception as err:
            print('\n', link.strip())

        # break

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

                # _type_name = ''
                # for type_name in property_type:
                #     _type_name += '_' + type_name

                property_list.to_csv(path_files + '/' + web + "_" + prop_type + '.csv')
                print('Export', len(ids), 'Rows To CSV File Completed!!!! ')
                print('Start At ', _start_date)
                print('Success At ', datetime.now())

                # break

            # send line message on success.
            fn.send_message(date, web)




