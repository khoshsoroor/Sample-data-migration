from collections import OrderedDict
from all import setting
import requests
import simplejson as json
import xlrd
import inflect


# region Data into db
def write_messages():
    auth_data = {"code": "666666", "mobile": "01117179264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    print(auth_id)
    workbook = xlrd.open_workbook(setting.path_msg)
    sheet = workbook.sheet_by_name('messages')
    for row in range(1, sheet.nrows):
        data = {}
        message_data = {}
        row_values = sheet.row_values(row)
        event_slug = row_values[0]
        # data['slug'] = event_slug
        # data['title'] = row_values[1]
        # data['is_enabled'] = bool(row_values[2])
        # res = requests.post(f'{setting.base_api_uri}/events', json=data, headers={'Authorization': f"Bearer {auth_id}"})
        # print(data)
        # print(res.json)
        message_data['event'] = event_slug
        message_data['is_enabled'] = bool(int(row_values[5]))
        message_data['template'] = row_values[4]
        message_data['type'] = row_values[3]
        print(json.dumps(message_data))
        check = requests.post(f'{setting.base_api_uri}/events/{event_slug}/announcements', json=message_data,headers={'Authorization': f"Bearer {auth_id}"})
        print(check.json)
    return "down"
# endregion
