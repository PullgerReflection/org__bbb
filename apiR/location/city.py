from pullgerReflection.org__bbb import models
from pullgerReflection.org__bbb import apiR


def add_city(id_name, description, country, state, *args, **kwargs):
    return models.City.add(id_name=id_name, description=description, country=country, state=state)


def get_city_count(*args, **kwargs):
    return models.City.objects.get_count()


def get_city_all(*args, **kwargs):
    return models.City.objects.get_all()


def get_city_by_id_name(
        country=None,
        id_iso_country=None,
        state=None,
        id_iso_state=None,
        id_name=None,
        id_name_city=None,
        **kwargs):
    if id_iso_country is not None:
        issue_country = apiR.get_country_by_iso(id_iso_country)
    else:
        issue_country = country

    if id_iso_state is not None:
        issue_state = apiR.get_state_by_iso(id_iso_state)
    else:
        issue_state = state

    if id_name is not None:
        issue_id_name = id_name
    else:
        issue_id_name = id_name_city

    return models.City.objects.get_by_keys(country=issue_country, state=issue_state, id_name=issue_id_name)
