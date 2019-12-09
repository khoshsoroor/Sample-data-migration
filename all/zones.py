import json
from collections import OrderedDict

import geojson
import requests
import simplejson as json
import xlrd
from shapely.geometry import Point

from all import setting, logger


# region Data into db
def write_zones():
    auth_data = {"code": "666666", "mobile": "09207078264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    logger.info(auth_id, extra={'appname': 'auth id is:'})
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('Zones')
    set_enabled = True

    for row in range(1, sheet.nrows):
        data = OrderedDict()
        row_values = sheet.row_values(row)
        city_slug = row_values[0]
        print(city_slug)
        data['slug'] = row_values[1]
        data['title'] = row_values[2].strip()
        data['is_enabled'] = set_enabled
        data['location'] = json.loads(geojson.dumps(Point(*map(float, row_values[4].split(",")))))
        print(data)
        res = requests.post(f"{setting.base_api_uri}/cities/{city_slug}/zones",
                            headers={'Authorization': f"Bearer {auth_id}"}, json=data)
        print(res.json)

    return "down"

# endregion
