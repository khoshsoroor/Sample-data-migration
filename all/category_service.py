
from collections import OrderedDict
from all import setting
import requests
import simplejson as json
import xlrd


# region Data into db
def write_categories_services():
    auth_data = {"code": "666666", "mobile": "01017159264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)

    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    print(auth_id)
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('Services')

    for row in range(1, sheet.nrows):
        row_values = sheet.row_values(row)
        service_slug = row_values[1]
        category_slug = row_values[0]
        print(service_slug)
        print(category_slug)
        res = requests.put(f"{setting.base_api_uri}/categories/{category_slug}/services/{service_slug}", headers={'Authorization': f"Bearer {auth_id}"})
        print(res.json)

    return "down"


# endregion


# write_categories_services()