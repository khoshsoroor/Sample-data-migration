from collections import OrderedDict
from all import setting
import requests
import simplejson as json
import xlrd
from all import logger


# region Data into db
def write_categories():
    auth_data = {"code": "666666", "mobile": "01117178264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    print(auth_id)
    logger.info(auth_id, extra={'appname': 'auth id is:'})
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('Categories-subcategories')

    for row in range(1, sheet.nrows):
        data = OrderedDict()
        row_values = sheet.row_values(row)
        data['parent_slug'] = row_values[0]
        if row_values[1] == row_values[0]:
            logger.info(row_values[1], extra={'appname': 'conflict slug category is:'})
        data['slug'] = row_values[1]
        data['title'] = row_values[2].strip()
        data['tags'] = row_values[3].split(",")
        if len(row_values[4]) >= 1:
            try:
                file_upload = f"{setting.path_categories_icon_logo_dir + row_values[4]}"
                my_file = open(file_upload, 'rb')
                upload_icon = requests.post(f"{setting.base_api_uri}/buckets/images/files", files={"file": my_file})
                logger.info(upload_icon.status_code, extra={'appname': 'response code for upload icon is:'})
                icon_code = upload_icon.json()
                icon_id = icon_code['file_id']
                logger.info(icon_id, extra={'appname': 'file id icon is:'})
                icon_url = f"/buckets/images/files/{icon_id}"
                data['icon'] = icon_url
            except:
                logger.info(row_values[4], extra={'appname': 'there is not this icon:'})

        if len(row_values[5]) >= 1:
            try:
                file_upload = f"{setting.path_categories_icon_logo_dir + row_values[5]}"
                my_file = open(file_upload, 'rb')
                upload_logo = requests.post(f"{setting.base_api_uri}/buckets/images/files", files={"file": my_file})
                logger.info(upload_logo.status_code, extra={'appname': 'response code for upload logo is:'})
                logo_code = upload_logo.json()
                logo_id = logo_code['file_id']
                logger.info(logo_id, extra={'appname': 'file id logo is:'})
                logo_url = f"/buckets/images/files/{logo_id}"
                data['logo'] = logo_url
            except:
                logger.info(row_values[5], extra={'appname': 'There is not this logo:'})

        if len(row_values[6]) >= 1:
            try:
                file_upload = f"{setting.path_categories_images_dir + row_values[6]}"
                my_file = open(file_upload, 'rb')
                upload_image = requests.post(f"{setting.base_api_uri}/buckets/images/files", files={"file": my_file})
                logger.info(upload_image.status_code, extra={'appname': 'response code for upload categories image is:'})
                image_code = upload_image.json()
                image_id = image_code['file_id']
                logger.info(image_id, extra={'appname': 'file id categories image is:'})
                image_url = f"/buckets/images/files/{image_id}"
                data['image'] = image_url
            except:
                print(f"image {row_values[6]} not found")
                logger.info(row_values[6], extra={'appname': 'There is not this image from categories:'})

        data['description'] = row_values[7].strip()
        integer_index = int(row_values[8] or '0')
        data['index'] = integer_index
        data['is_enabled'] = bool(row_values[9])
        categories_slug = data['slug']
        print(data)
        res = requests.post(f"{setting.base_api_uri}/categories",  headers={'Authorization': f"Bearer {auth_id}"},json=data)
        # print(res)
        print(res.json)

    return "down"

# endregion
