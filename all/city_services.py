from collections import OrderedDict
from all import setting
import requests
import simplejson as json
import xlrd


# region Data into db
def write_city_services():
    auth_data = {"code": "666666", "mobile": "01117079264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    print(auth_id)
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('Cities-services')
    print(sheet)
    # set_enabled = True
    for row in range(1, sheet.nrows):
        data = OrderedDict()
        row_values = sheet.row_values(row)
        city_slug = row_values[0]
        service_slug = row_values[3]
        if row_values[4] == "MALE":
            data['gender'] = "Male"
        if row_values[4] == "FEMALE":
            data['gender'] = "Female"
        data['is_enabled'] = bool(row_values[2])
        data['skip_time'] = row_values[7]
        data['finish_at'] = row_values[6]
        data['start_at'] = row_values[5]
        print(service_slug)
        print(json.dumps(data))
        res = requests.put(f"{setting.base_api_uri}/cities/{city_slug}/services/{service_slug}/details",
                           headers={'Authorization': f"Bearer {auth_id}"}, json=data)
        print(res.json)

    return "down"

# endregion
