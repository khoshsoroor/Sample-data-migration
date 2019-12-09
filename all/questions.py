from itertools import groupby
import requests
import simplejson as json
import xlrd
from all import setting, logger


# region Data into db
def write_questions():
    auth_data = {"code": "666666", "mobile": "09127179264"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_code= input("Enter code")
    my_data= {"code": get_code, "mobile": "09127179264"}
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=my_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    print(auth_id)
    logger.info(auth_id, extra={'appname': 'auth id is:'})
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('q')

    for k, g in groupby((sheet.row(i) for i in range(1, sheet.nrows)),
                        lambda q: q[1].value if type(q[1]) != str else None):
        if k:
            records = list(g)
            service_slug = records[0][0].value
            print(service_slug)
            logger.info(service_slug, extra={'appname': 'service slug is:'})
            question = {'slug': records[0][1].value, 'title': records[0][2].value, 'question_type': records[0][3].value,
                        'is_required': bool(int(records[0][4].value)), 'is_first': bool(int(records[0][5].value)),
                        'description': records[0][6].value,
                        'next_question': records[0][7].value, 'choices': [
                    {'description': c[8].value, 'index': int(c[9].value or '0'), 'next_question': c[10].value,
                     'title': c[11].value,
                     'tooltip': c[12].value} for c in records]}
            print(question['slug'])
            if records[0][3].value == "SINGLE_SELECT":
                question['question_type'] = "SingleChoice"
            if records[0][3].value == "MULTIPLE_SELECT":
                question['question_type'] = "MultiChoice"
            if records[0][3].value == "TEXT":
                question['question_type'] = "Descriptive"
            logger.info(question['slug'], extra={'appname': 'question slug is:'})
            q_slug = question.get('slug')
            if len(q_slug) > 25:
                print(f"slug is larger than 25 char is: {q_slug}")
                logger.error(q_slug, extra={'appname': 'slug is larger than 25 char is:'})
            logger.info(json.dumps(question, ensure_ascii=False), extra={'appname': 'question data:'})
            res = requests.post(f"{setting.base_api_uri}/services/{service_slug}/questions", json=question,
                                headers={"Authorization": f"Bearer {auth_id}"})

            print(res.json)
            logger.info(res.status_code, extra={'appname': 'status code for post question:'})
    write_next_question()


# endregion


# region Data into db
def write_next_question():
    auth_data = {"code": "666666", "mobile": "09121404958"}
    auth = requests.post(f"{setting.base_api_uri}/authenticates", json=auth_data)
    get_code = input("Enter code")
    my_data = {"code": get_code, "mobile": "09121404958"}
    get_id = requests.post(f"{setting.base_api_uri}/authenticates", json=my_data)
    get_id_json = get_id.json()
    auth_id = get_id_json['code']
    logger.info(auth_id, extra={'appname': 'auth id is:'})
    workbook = xlrd.open_workbook(setting.path_excel)
    sheet = workbook.sheet_by_name('q')
    for k, g in groupby((sheet.row(i) for i in range(1, sheet.nrows)),
                        lambda q: q[1].value if type(q[1]) != str else None):
        if k:
            records = list(g)
            service_slug = records[0][0].value
            logger.info(service_slug, extra={'appname': 'service slug for put is:'})

            question = {'slug': records[0][1].value, 'title': records[0][2].value,'question_type': records[0][3].value,
                        'is_required': bool(int(records[0][4].value)), 'is_first': bool(int(records[0][5].value)),
                        'description': records[0][6].value,
                        'next_question': records[0][7].value, 'choices': [
                    {'description': c[8].value, 'index': int(c[9].value or '0'), 'next_question': c[10].value,
                     'title': c[11].value,
                     'tooltip': c[12].value} for c in records]}
            if records[0][3].value == "SINGLE_SELECT":
                question['question_type'] = "SingleChoice"
            if records[0][3].value == "MULTIPLE_SELECT":
                question['question_type'] = "MultiChoice"
            if records[0][3].value == "TEXT":
                question['question_type'] = "Descriptive"
            question_slug = question['slug']
            logger.info(question_slug, extra={'appname': 'question slug for put is:'})
            logger.info(json.dumps(question, ensure_ascii=False), extra={'appname': 'question data for put is:'})
            change = requests.put(f"{setting.base_api_uri}/services/{service_slug}/questions/{question_slug}",
                                  json=question, headers={"Authorization": f"Bearer {auth_id}"})

            logger.info(change.status_code, extra={'appname': 'status code for put question:'})
# endregion
