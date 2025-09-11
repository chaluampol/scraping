import pandas as pd
import datetime
import os
import platform
import requests
from dotenv import load_dotenv
from pathlib import Path
import matplotlib.pyplot as plt


# print(platform.system())
# Windows
# Darwin

load_dotenv()


prv_list = pd.read_csv('Region/TBL_Province.csv')
dis_list = pd.read_csv('Region/TBL_District.csv')
subdis_list = pd.read_csv('Region/TBL_SUB_District.csv')
new_subdis_list = subdis_list.drop_duplicates(subset={'DISTRICT_CODE', 'DISTRICT_NAME', 'Amphur_code', 'PROVINCE_code'}, keep='first', inplace=False)

source =   [{'id': 1, 'name': 'home'},
            {'id': 2, 'name': 'ddproperty'},
            {'id': 3, 'name': 'baanfinder'},
            {'id': 4, 'name': 'kaidee'},
            {'id': 5, 'name': 'baania'},
            {'id': 6, 'name': 'zmyhome'},
            {'id': 7, 'name': 'sam'},
            {'id': 8, 'name': 'bam'},
            {'id': 9, 'name': 'led'},
            {'id': 10, 'name': 'terrabkk'},
            {'id': 11, 'name': 'hometophit'},
            {'id': 12, 'name': 'thaihomeonline'},
            {'id': 13, 'name': 'dotproprety'},
            {'id': 14, 'name': 'prakardproprety'},
            {'id': 15, 'name': 'klungbaan'},
            {'id': 16, 'name': 'posttoday'},
            {'id': 24, 'name': 'bangkokassets'},
            {'id': 25, 'name': 'propertyscout'},
            {'id': 26, 'name': 'propertyhub'},
            {'id': 27, 'name': 'TheBestProperty'},
            {'id': 0, 'name': 'ไม่ทราบ'}]

def get_range_of_price(price):
    try:
        if price != 0.0:
            if float(price) < 1000000:
                return 1
            elif float(price) <= 1500000:
                return 2
            elif float(price) <= 2000000:
                return 3
            elif float(price) <= 3000000:
                return 4
            elif float(price) <= 5000000:
                return 5
            elif float(price) <= 7500000:
                return 6
            elif float(price) <= 10000000:
                return 7
            else:
                return 8
        else:
            return 0
    except:
        return 0

def get_lim_bed_bath(type_id):
    lim_bed_bath = {
        1: 30,
        2: 20,
        3: 20
    }
    return lim_bed_bath[type_id]


def get_location(house_address):
    section_words = house_address.replace("(", "").replace(")", "").replace("-", "").replace(".", "").split(",")
    count = 0
    for i in range(len(section_words) - 1, -1, -1):
        count += 1
        word = section_words[i].strip()

        if count == 1:
            _province = word

        if count == 2:
            _district = word

        if count == 3:
            _subdistrict = word

        if count == 3:
            break

    return prov_dis_subdis(_province, _district, _subdistrict)

def get_location_hometophit(_address):
    _new_address = _address.replace("(", "").replace(")", "").replace("-", " ").replace(".", "").replace('  ', ' ')
    _address_list = _new_address.replace('จังหวัด', '').replace('จ.', '').replace('อำเภอ', '').replace('อ.',
                                                                                                       '').replace(
        'เขต', '').replace('ตำบล', '').replace('ต.', '').split(' ')

    prv_name = ''
    dis_name = ''
    sub_dis_name = ''
    for i in _address_list:
        if i.strip() == 'กรุงเทพ' or i.strip() == 'กรุงเทพฯ':
            i = 'กรุงเทพมหานคร'

        try:
            prv_name = prv_list[prv_list['PROVINCE_NAME'] == i.strip()]['PROVINCE_NAME'].item()
        except:
            ''

        try:
            dis_name = dis_list[dis_list['AMPHUR_Name'] == i.strip()]['AMPHUR_Name'].item()
        except:
            ''

        try:
            sub_dis_name = new_subdis_list[new_subdis_list['DISTRICT_NAME'] == i.strip()]['DISTRICT_NAME'].item()
        except:
            ''

    return prov_dis_subdis(prv_name, dis_name, sub_dis_name)

def prov_dis_subdis(prv, dis, subdis):
    prv = clean(prv)
    dis = clean(dis)
    subdis = clean(subdis)

    if prv == 'กรุงเทพ' or prv == 'กรุงเทพฯ':
        prv = 'กรุงเทพมหานคร'

    try:
        prv_code = prv_list[prv_list['PROVINCE_NAME'] == prv]['PROVINCE_CODE'].item()
    except:
        prv_code = 0

    try:
        dis_code = dis_list[(dis_list['PROVINCE_code'] == prv_code) &
                            (dis_list['AMPHUR_Name'] == dis)]['AMPHUR_CODE'].item()
    except:
        dis_code = 0

    try:
        subdis_code = new_subdis_list[(new_subdis_list['PROVINCE_code'] == prv_code) &
                                  (new_subdis_list['Amphur_code'] == dis_code) &
                                  (new_subdis_list['DISTRICT_NAME'] == subdis)]['DISTRICT_CODE'].item()
    except:
        subdis_code = 0

    return str(prv_code)[0: 2], str(dis_code)[0: 4], str(subdis_code)[0: 6]


def get_sell_typeID(sell_type):
    if sell_type.find("ขาย") >= 0 and sell_type.find("เช่า") == -1:
        return 1
    elif sell_type.find("ขาย") == -1 and sell_type.find("เช่า") >= 0:
        return 2
    else:
        return 0

def get_source_id(web):
    try:
        for names in source:
            if web == names['name']:
                return names['id']
    except:
        return 0

def get_date_now():
    return datetime.datetime.now().strftime('%Y-%m-%d')

def clean(x):
    junks = ['_newline','.','-','_',':',';','*','\'','/','(',')','เขต','แขวง']
    for junk in junks:
        x = x.replace(junk,'')
    return x

def remove_from_list(x, l, z=''):
    for y in l:
        x = x.replace(y, z)
    return x

def get_floor(name, detail):
    keywords = ['โครงการ', 'หมู่บ้าน']
    commons = ['รายละเอียด', 'ชุมชน', 'เพิ่มเติม', 'สอบถาม', 'ข้อมูล', 'สนใจ', 'ต่อเติม', 'หลังบ้าน', 'ห้องนอน',
               'ห้องครัว', 'จอดรถ', 'ติดต่อ', 'ทำเล', 'สะดวกสบาย', 'สะดวก', 'เพียงแค่', 'อยู่หลัง', 'ทำเล', 'ใจกลาง']
    commons += ['housename', 'housedetail', 'ขาย', 'ทาวน์เฮ้าส์', 'หมู่บ้าน', 'ที่ตั้ง', 'เนื้อที่', 'ตรว', 'ตารางวา',
                'ติดกับ', 'ใน', 'และกำลังขึ้น', 'ซอย', '\n']

    detail = clean(name + ' ' + detail)
    detail = remove_from_list(detail, keywords)
    detail = remove_from_list(detail.strip(), commons)
    floor = -1
    fidx = detail.find('ชั้น')
    if fidx >= 0:
        fl = detail[fidx:fidx + 8]
        fl = "".join(filter(str.isdigit, fl))
        floor = fl
    fidx = detail.find('floor')
    if fidx >= 0:
        fl = detail[fidx - 8:fidx]
        fl = "".join(filter(str.isdigit, fl))
        floor = fl
    if floor == "":
        return 'none'
    return int(floor)


def build_massage(date: str, web: str):
    project_root = Path(__file__).resolve().parent
    path_link = str(project_root) + "/links/" + date + "/"  + web + "/"
    path_data = str(project_root) + "/Files/" + date + "/"  + web + "/"
    path_logs = str(project_root) + "/logs/"+ date + "_" + web + "_result_table.txt"

    files = [f for f in os.listdir(path_link) if os.path.isfile(os.path.join(path_link, f))]

    _noti_massage = ""
    _noti_massage += "##### " + date + " : "+ web + " #####"
    property_type = []
    for file in files:
        _property_type = str(file).replace("links_", "").replace("link_", "").replace(".txt", "")
        property_type.append(_property_type)

        _data_msg = ""
        _data_len = 0
        try:
            file_data_path = Path(path_data + '/' + web + "_" + _property_type + ".csv")
            data_lines = file_data_path.read_text().splitlines()
            _data_len = len(data_lines)
            _data_msg = "Data: " + "{:,}".format(_data_len - 1)
        except:
            _data_msg = "Data: 0"

        _link_msg = ""
        try:
            file_links_path = Path(path_link + '/' + file)
            link_lines = file_links_path.read_text().splitlines()
            _link_msg = "Link: " + "{:,}".format(len(link_lines))
        except:
            _link_msg = "Link: 0"

        _icon = "✅ " if _data_len > 0 else "❌ "
        _noti_massage += "\n" + _icon + _property_type
        _noti_massage += "\n=> " + " " + _link_msg + " " +  _data_msg

    with open(path_logs, "r", encoding="utf-8") as f:
        content = f.read()
        _noti_massage += "\n" + content

    _noti_massage += "\n##### " + web + " #####"
    return _noti_massage

def send_message(date: str, web: str):
    line_channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    line_user_id = os.getenv("LINE_USER_ID")

    _noti_message = build_massage(date, web)

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {line_channel_access_token}"
    }
    data = {
        "to": line_user_id,
        "messages": [{"type": "text", "text": _noti_message}]
    }

    res_line_msg = requests.post(url, headers=headers, json=data)
    if res_line_msg.status_code == 200:
        print("Line: Message sent successfully!")
    else:
        print(f"Line: Failed to send message: {res_line_msg.status_code}, {res_line_msg.text}")

def check_data(date: str, web: str):
    data_of_web_list = {
        "baanfinder": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price', 'area_SQW', 'area_SQM', 'sell_type_id', 'bedroom', 'bathroom', 'garage', 'detail', 'latitude', 'longtitude', 'picture', 'source_id', 'house_link', 'seller_name', 'seller_tel', 'floor', 'floor_number', 'completion_year'],
        "baania": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price', 'area_SQM', 'area_SQW', 'seller_tel', 'seller_name', 'seller_email', 'sell_type_id', 'room_number', 'bedroom', 'bathroom', 'garage', 'detail', 'latitude', 'longtitude', 'floor', 'floor_number', 'picture'],
        "bangkokassets": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price', 'picture', 'bedroom', 'bathroom', 'detail', 'latitude', 'longtitude', 'area_SQM', 'area_SQW', 'floor', 'floor_number', 'seller_name', 'seller_tel', 'seller_email'],
        "ddproperty": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price', 'picture', 'area_SQW', 'area_SQM', 'bedroom', 'bathroom', 'latitude', 'longtitude', 'floor_number', 'seller_name', 'seller_email', 'seller_tel', 'completion_year'],
        "dotproprety": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture', 'bedroom', 'bathroom', 'area_SQW', 'area_SQM', 'detail', 'floor', 'floor_number', 'seller_name'],
        "fazwaz": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture', 'area_SQM', 'area_SQW', 'bedroom', 'bathroom', 'garage', 'completion_year', 'floor', 'floor_number', 'detail'],
        "homemarket": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture', 'area_SQW', 'area_SQM', 'seller_name', 'seller_tel', 'bedroom', 'bathroom', 'detail'],
        "hongpak": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture', 'area_SQM', 'area_SQW', 'bedroom', 'bathroom', 'floor', 'floor_number', 'detail', 'seller_tel', 'latitude', 'longtitude'],
        "interhome": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture', 'bedroom', 'bathroom', 'area_SQM', 'area_SQW', 'detail', 'seller_name', 'seller_tel', 'floor', 'latitude', 'longtitude'],
        "kaidee": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture', 'bedroom', 'bathroom', 'area_SQW', 'area_SQM', 'detail', 'seller_name', 'seller_tel', 'seller_email', 'latitude', 'longtitude'],
        "klungbaan": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture', 'area_SQM', 'area_SQW', 'floor_number', 'floor', 'bedroom', 'bathroom', 'garage', 'detail', 'latitude', 'longtitude', 'seller_name', 'seller_tel', 'seller_email'],
        "livinginsider": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture','area_SQW', 'area_SQM', 'bedroom', 'bathroom', 'floor', 'floor_number', 'detail', 'seller_name', 'latitude', 'longtitude'],
        "propertyhub": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'range_of_house_price','picture','bedroom', 'bathroom', 'area_SQW', 'area_SQM', 'detail', 'seller_name', 'seller_tel', 'latitude', 'longtitude'],
        "propertyscout": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'bedroom', 'bathroom', 'detail', 'latitude', 'longtitude', 'area_SQM', 'area_SQW', 'floor', 'floor_number'],
        "terrabkk": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price','area_SQW', 'area_SQM', 'bedroom', 'bathroom', 'garage', 'detail', 'latitude', 'longtitude', 'seller_name', 'seller_tel', 'floor', 'floor_number'],
        "thaihometown": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'area_SQM', 'area_SQW', 'bedroom', 'bathroom', 'latitude', 'longtitude', 'garage', 'detail', 'seller_name', 'seller_tel'],
        "thaihometownland": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'ref_code', 'area_SQW', 'bedroom', 'bathroom', 'latitude', 'longtitude', 'garage', 'detail', 'seller_name', 'seller_tel'],
        "TheBestProperty": ['name', 'project_name', 'address', 'province_code', 'district_code', 'subdistrict_code', 'price', 'bedroom', 'bathroom', 'area_SQW', 'area_SQM', 'detail', 'floor', 'floor_number', 'latitude', 'longtitude']
    }

    web_process = data_of_web_list[web]

    project_root = Path(__file__).resolve().parent
    path_link = str(project_root) + "/links/" + date + "/"  + web + "/"
    path_data = str(project_root) + "/Files/" + date + "/"  + web + "/"
    files = [f for f in os.listdir(path_link) if os.path.isfile(os.path.join(path_link, f))]

    # DataFrame สำหรับรวมผลลัพธ์
    result_df = pd.DataFrame({"Column": web_process})

    # วนลูปแต่ละไฟล์
    for file_path in files:
        _property_type = str(file_path).replace("links_", "").replace("link_", "").replace(".txt", "")
        file_data_path = Path(path_data + '/' + web + "_" + _property_type + ".csv")
        df = pd.read_csv(file_data_path)
        # file_name = os.path.basename(file_data_path)  # ดึงเฉพาะชื่อไฟล์
        
        # คำนวณ %
        percentages = {}
        for col in web_process:
            if col in df.columns:
                total = len(df)
                not_none_count = (df[col].astype(str).str.lower() != 'none').sum()
                percentages[col] = round((not_none_count / total) * 100, 2)
            else:
                percentages[col] = None  # ถ้าไม่มี column นี้
        
        # แปลงเป็น DataFrame แล้ว merge
        temp_df = pd.DataFrame(list(percentages.items()), columns=["Column", _property_type])
        result_df = result_df.merge(temp_df, on="Column", how="left")

    print(result_df)

    path_logs = os.path.join("logs")
    os.makedirs(path_logs, exist_ok=True)

    output_txt_path = str(project_root) + "/logs/"+ date + "_" + web + "_result_table.txt"
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write("```\n" + result_df.to_string(index=False) + "\n```")