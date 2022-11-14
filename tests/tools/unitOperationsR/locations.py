from django.test import TestCase
from pullgerReflection.org__bbb import apiR
from pullgerReflection.org__bbb.tests.tools import dataTemplatesR

from pullgerReflection.org__bbb.models import models_locations


def add_country(self: TestCase):

    country_element_data_list = dataTemplatesR.country_data()
    for country_element_data in country_element_data_list:
        apiR.add_country(**country_element_data)

        new_element = apiR.get_country_by_iso(**country_element_data)

        for (key, value) in country_element_data.items():
            self.assertEqual(getattr(new_element, key), value, "Incorrect compare DATA in new object")


def add_state(self: TestCase):
    add_country(self)
    data_list = dataTemplatesR.state_data()
    for data_element in data_list:
        country_element = apiR.get_country_by_iso(id_iso_country=data_element["id_iso_country"])
        new_element = apiR.add_state(country=country_element, **data_element)

        issue_element = apiR.get_state_by_iso(country=country_element, **data_element)
        for (key, value) in data_element.items():
            self.assertEqual(getattr(issue_element, key), value, "Incorrect compare DATA in new object")


def add_city(self: TestCase):
    add_state(self)

    data_list = dataTemplatesR.city_data()
    for data_element in data_list:
        country_element = apiR.get_country_by_iso(data_element["id_iso_country"])
        state_element = apiR.get_state_by_iso(id_iso=data_element["id_iso_state"], country=country_element)

        new_city = apiR.add_city(country=country_element, state=state_element, **data_element)
        self.assertIsInstance(new_city, models_locations.City, "Incorrect on creating 'City'")

        issue_element = apiR.get_city_by_id_name(**data_element)

        for (key, value) in data_element.items():
            self.assertEqual(getattr(issue_element, key), value, "Incorrect compare DATA in new object")

    return issue_element
