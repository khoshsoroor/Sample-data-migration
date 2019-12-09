from collections import OrderedDict
from all import setting
import requests
import simplejson as json
import xlrd


# region Data into db
def write_revenue():
    auth_data = {"code": "666666", "mobile": "01117150064"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    print(auth_id)
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('Cities-services')
    for row in range(1, sheet.nrows):
        data = OrderedDict()
        row_values = sheet.row_values(row)
        if bool(row_values[2]):
            data["ceiling"]= int(row_values[8])
            data["city_slug"] = row_values[0]
            data["service_slug"] = row_values[3]
            data['model'] = row_values[9]
            data['slug'] = row_values[10]
            data['value'] = int(row_values[11])
            if row_values[12] == "amount":
                data['value_type'] = "Amount"

            revenues_slug = row_values[10]
            res = requests.post(f"{setting.base_api_uri}/revenues",
                            headers={'Authorization': f"Bearer {auth_id}"}, json=data)
            print(res)
    return "down"
# endregion