
from collections import OrderedDict

import geojson
import json
from all import setting
import requests
import simplejson as json
import xlrd
from shapely.geometry import Point


# region Data into db
def write_city_offices():
    # Open the workbook and select the first worksheet
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('City_offices')
    print(sheet)
    # List to hold dictionaries
    set_enabled = True
    auth_data = {"code": "666666", "mobile": "01017179264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    print(auth)
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    # print(get_id.json())
    get_id_json = get_id.json()
    # print(get_id_json)
    auth_id = get_id_json['code']
    print(auth_id)
    for row in range(1, sheet.nrows):
        data = OrderedDict()
        row_values = sheet.row_values(row)
        city_slug = row_values[0]
        data['slug'] = row_values[1]
        data['is_enabled'] = set_enabled
        data['title'] = row_values[2]
        data['address'] = row_values[3]
        data['zip_code'] = str(row_values[4])
        data['phone_number'] = row_values[5]
        data['location'] = json.loads(geojson.dumps(Point(*map(float, row_values[6].split(",")))))
        print(json.dumps(data , ensure_ascii=False))
        res = requests.post(f"{setting.base_api_uri}/cities/{city_slug}/offices", json=data, headers={'Authorization':f"Bearer {auth_id}"})
        print(res.json)

    return "down"

# endregion
