from collections import OrderedDict
from all import setting ,logger
import requests
import simplejson as json
import csv
import codecs
import xlrd


# region Data into db
def write_banner_image():
    auth_data = {"code": "666666", "mobile": "09127179205"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    # num = input("Enter number :")
    # auth_data['code']= num
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    logger.info(auth_id, extra={'appname': 'auth id is:'})
    workbook = xlrd.open_workbook(setting.banner_excel)
    sheet = workbook.sheet_by_name('Homepage-banners')
    set_enabled = True
    for row in range(1, sheet.nrows):
        data = dict()
        row_values = sheet.row_values(row)
        data['slug'] = row_values[1]
        data['title'] = row_values[2].strip()
        data['tags'] = row_values[7].split(",")
        data['is_enabled'] = set_enabled
        result = json.loads(row_values[3])
        print(result['image'])
        if result['image']:
            file_upload = f"{setting.path_banners_image_dir}" + result['image']
            logger.info(file_upload, extra={'appname': 'direction is:'})
            my_file = open(file_upload, 'rb')
            response = requests.post(f"{setting.base_api_uri}/buckets/images/files", files={"file": my_file})
            logger.info(response.text, extra={'appname': 'post image is:'})
            image_code = response.json()
            image_id = image_code['file_id']
            image_url = f"/buckets/images/files/{image_id}"
            result['image'] = image_url
        logger.info(result, extra={'appname': 'result is:'})
        data['data'] = result
        logger.info(data, extra={'appname': 'all data is:'})

        banner_slug = row_values[1]
        res = requests.post(f'{setting.base_api_uri}/banners', json=data,headers={'Authorization': f"Bearer {auth_id}"})
        if res.status_code == 201:
            logger.info(res.status_code, extra={'appname': 'success code:'})
        else:
            logger.error(res.status_code,extra={'appname': 'failed code is:'})
# endregion

