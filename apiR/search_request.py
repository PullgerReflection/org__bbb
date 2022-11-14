from pullgerReflection.org__bbb import models
from pullgerReflection.org__bbb import apiR


def add_search_request(city, category, *args, **kwargs):
    return models.SearchRequests.add(category=category, city=city)


def get_search_request_by_ids(id_iso_country, id_iso_state, id_name_city, id_name_category, *args, **kwargs):
    country = apiR.get_country_by_iso(id_iso=id_iso_country)
    state = apiR.get_state_by_iso(id_iso=id_iso_state)
    city = apiR.get_city_by_id_name(country=country, state=state, id_name=id_name_city)
    category = apiR.get_category_by_id_name(id_name=id_name_category)
    return models.SearchRequests.objects.get_by_sub_keys(city=city, category=category)


def accordance_search_requests():
    counter_create = 0
    for city_fetch in apiR.get_city_all():
        for category_fetch in apiR.get_category_all():
            add_search_request(city=city_fetch, category=category_fetch)
            counter_create += 1
    return counter_create
