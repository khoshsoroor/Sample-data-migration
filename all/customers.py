from io import BytesIO

import geojson
import requests
import simplejson as json
from pymongo import MongoClient
from shapely.geometry import Point

from all import setting, logger

client = MongoClient('localhost', 27017)
db = client.ostadkar
customers = db.customers


# region Data into db
def write_customer():
    for item in customers.find().sort([("registrationDate", -1)]):
        user = item.get('username') or item.get('userName')
        logger.info(user, extra={'appname': 'user name is:'})
        auth_data = {"code": "666666", "mobile": user}
        auth = requests.post("https://api.dev.ostadkar.pro/authenticates", json=auth_data)
        get_id = requests.post("https://api.dev.ostadkar.pro/authenticates", json=auth_data)
        get_id_json = get_id.json()
        auth_id = get_id_json['code']
        # print(item)
        print(item['username'])
        logger.info(auth_id, extra={'appname': 'auth id is:'})
        users = {'mobile': user, 'roles': []}
        # print(json.dumps(users))
        result_users = requests.post(f"{setting.base_api_uri}/users", json=users,
                                     headers={'Authorization': f"Bearer {auth_id}"})
        print(result_users)
        data_customer = {}
        if item.get('firstName'):
            data_customer["first_name"] = item['firstName']
        else:
            print(f"there is not first name for {user}")
            data_customer["first_name"] = "NoName"
        if item.get('lastName'):
            data_customer["last_name"] = item['lastName']
        else:
            print(f"there is not last name for {user}")
            data_customer["last_name"] = "NoName"
        if item.get('nationalCode'):
            data_customer["national_code"] = item['nationalCode']
        else:
            print(f"there is not national code for {user}")
            data_customer["national_code"] = "1234567890"
        if item.get('profilePicture'):
            file_upload = requests.get(f"{setting.base_api_uri}/media/" + item['profilePicture'])
            my_file = file_upload.content

            upload_pic = requests.post(f"{setting.base_api_uri}/buckets/images/files",
                                       files={"file": BytesIO(my_file)})
            logger.info(upload_pic.text, extra={'appname': 'response code for upload pic is:'})
            profile_code = upload_pic.json()
            upload_id = profile_code['file_id']
            logger.info(upload_id, extra={'appname': 'file id pic is:'})
            picture_url = f"/buckets/images/files/{upload_id}"
            data_customer["picture"] = picture_url
        else:
            print(f"there is not picture for {user}")
            data_customer["picture"] = "123456"
        # print(data_customer)
        add_customer = requests.put(f"{setting.base_api_uri}/customers/me", json=data_customer,
                                    headers={'Authorization': f"Bearer {auth_id}"})
        print(add_customer)
        delivery_customer = {}
        address = item.get("addressList")
        # print(address)
        if address:
            for rows in address:
                zone_point = json.loads(geojson.dumps(Point(rows.get('latitude'), rows.get('longitude'))))
                # print(zone_point)
                city_slug = rows.get('citySlug')
                delivery_customer = {'title': rows['title'], "address": rows['address'], "city_slug": city_slug,
                                     "zone_slug": rows.get('neighborhood'), "location": zone_point}
                if not (rows['address']):
                    delivery_customer['address'] = "address not found"
                    print("delivery address not found")
                if not rows.get('neighborhood', []):
                    if rows.get('zone_slug'):
                        delivery_customer['zone_slug'] = rows.get('zone_slug')
                    delivery_customer['zone_slug'] = "zone not found"
                    print("zone not found")

                print(json.dumps(delivery_customer, ensure_ascii=False))
                add_delivery = requests.post(f"{setting.base_api_uri}/customers/me/deliveries", json=delivery_customer,
                                             headers={'Authorization': f"Bearer {auth_id}"})
                print(add_delivery.status_code)
# TODO zone slug
# zone_gets = requests.get(f"{setting.base_api_uri}/cities/{city_slug}/zones?$top=360")
# all_zones = zone_gets.json()
# print(all_zones['value'])

# for find_slug in all_zones['value']:
#     print(find_slug['title'])
#     print(delivery_customer.get('neighborhood'))
#     print(delivery_customer.get('zone_slug'))
#     if find_slug['title'] in delivery_customer.get('neighborhood',[]):
#         print("zone find")
#         print(find_slug['title'])
#         print(find_slug['slug'])
#     elif find_slug['title'] in delivery_customer.get('zone_slug',[]):
#         print("zone find")
#     else:
#         print("address not match")

# endregion
