
from collections import OrderedDict
from all import setting
import requests
import simplejson as json
import xlrd


# region Data into db
def write_users():
    # Open the workbook and select the first worksheet
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet_roles = workbook.sheet_by_name('user_roles')
    sheet_users = workbook.sheet_by_name('users')

    # for row in range(1, sheet_roles.nrows):
    #     data = OrderedDict()
    #     row_values = sheet_roles.row_values(row)
    #     data['slug'] = '-'.join(row_values[0].lower().strip().split())
    #     data['title'] = row_values[1].strip()
    #     print(data)
    #     result_roles = requests.post(f"{setting.base_api_uri}/roles", json=data)
    #     print(result_roles)
    for row_users in range(1, sheet_users.nrows):
        users = OrderedDict()
        users_values = sheet_users.row_values(row_users)
        users['mobile'] = users_values[0]
        users['roles'] = users_values[1].split(",")
        print(json.dumps(users))
        result_users = requests.post(f"{setting.base_api_uri}/users", json=users)
        print(result_users)

    return "down"


# endregion