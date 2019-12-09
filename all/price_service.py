import csv
from collections import OrderedDict
from all import setting
import requests
import simplejson as json
import xlrd
import uuid
from mako.template import Template
from htmlmin import minify
from all import logger
import markdown


def write_price_services():
    make_buckets = requests.put(f"{setting.base_api_uri}/buckets/images")
    print(make_buckets)
    auth_data = {"code": "666666", "mobile": "09127179264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    print(auth_id)
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('Services')
    for row in range(1, sheet.nrows):
        data = OrderedDict()
        row_values = sheet.row_values(row)
        data['category_slug'] = row_values[0]
        data['slug'] = row_values[1]
        data['title'] = row_values[2].strip()
        integer_index = int(row_values[3] or '0')
        data['index'] = integer_index
        data['summary'] = row_values[4]
        if len(row_values[5]) >= 1:
            try:
                file_upload = f"{setting.path_services_image_dir + row_values[5]}"

                my_file = open(file_upload, 'rb')

                upload_service_images = requests.post(f"{setting.base_api_uri}/buckets/images/files",
                                                      files={"file": my_file})
                logger.info(upload_service_images.status_code,
                            extra={'appname': 'upload service images status code is:'})
                # print(upload_service_images.json)
                service_image_code = upload_service_images.json()
                image_id = service_image_code['file_id']
                image_url = f"/buckets/images/files/{image_id}"
                data['image'] = image_url
            except Exception as e:
                logger.error(e, extra={'appname': f"image {row_values[5]} not found"})

        with open(setting.path_service_description) as description_file:
            json_load = json.load(description_file)
            for des in json_load:
                if row_values[6] == des['slug']:
                    md = markdown.Markdown()
                    md.convert(des['markdownDescription'])
                    data['description'] = des['markdownDescription']
                    print(data['description'])

        price = price_write(f'{setting.price_file}', row_values[6], "tehran")
        if price is None:
            logger.info(row_values[1], extra={'appname': "there is not price guide for this service:"})

            price = "<tr>there is not price guide</tr>"
        data['price_guide'] = price
        data['tips'] = row_values[8]
        data['tags'] = row_values[9].split(",")
        data['is_enabled'] = bool(row_values[10])
        service_slug = row_values[1]

        logger.info(json.dumps(data, ensure_ascii=False), extra={'appname': "data json:"})
        res = requests.put(f"{setting.base_api_uri}/services/{service_slug}", headers={'Authorization': f"Bearer {auth_id}"}, json=data)
        logger.info(res.status_code, extra={'appname': "post services status code is:"})

    return "down"


# endregion

# region price data
def price_write(path, service_slug, city_slug):
    with open(path, encoding='utf-8') as price_file:
        csv_reader = csv.reader(price_file, delimiter=',')

        row = next((r for r in csv_reader if r[5] == service_slug or r[6]== service_slug and r[2] == city_slug), None)
        if row:
            check_template = Template(filename='/home/mahsa/Documents/Ostadkar_Gitlab/ostadkar-data-migration/all'
                                               '/table_tmp.html.mako')
            data = json.loads(row[3])
            print(data)
            table = check_template.render(titles=['شرح خدمات','قیمت واحد(تومان)'],
                                          rows=[OrderedDict(caption=item['caption'],
                                                            text=item['text'] if item['type'] == 'TEXT' else (item.get(
                                                                'ok')*1000)) for item in data])

            # logger.info(table, extra={'appname': "table price is:"})
            mini_table = minify(table, remove_empty_space=True)
            logger.info(mini_table, extra={'appname': "mini table price is:"})
            # print(mini_table)

            return mini_table
# endregion
