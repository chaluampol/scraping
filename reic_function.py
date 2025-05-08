import pandas as pd
import datetime
import os
import platform


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



# print(platform.system())
# Windows
# Darwin