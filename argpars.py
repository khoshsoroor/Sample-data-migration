import argparse

from all import categories, services, category_service, banners, city_services, facilities, offices, messages, \
    questions, users, services_facility, zones,revenue , price_service

my_parser = argparse.ArgumentParser()
my_parser.add_argument('script_names', help='input name of script')
names = {'services': services.write_services, "banners": banners.write_banner_image,
         "categories": categories.write_categories,
         "categories_service": category_service.write_categories_services,
         "city_services": city_services.write_city_services, "facilities": facilities.write_facility,
         "offices": offices.write_city_offices, "messages": messages.write_messages,
         "question": questions.write_questions, "users": users.write_users,
         "service_facility": services_facility.write_service_facility, "zones": zones.write_zones,
         "revenue":revenue.write_revenue}
args = my_parser.parse_args()
print(args)
names[args.script_names]()


