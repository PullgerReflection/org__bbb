from pullgerReflection.com_linkedin import api
from pullgerReflection.com_linkedin.tests.tools import dataTemplatesR

from django.test import TestCase


def add_search(self: TestCase):

    search_data = dataTemplatesR.people_search_data()
    new_people_search = api.add_people_search(**search_data)

    for (keyData, valueData) in search_data.items():
        if keyData != "locations":
            self.assertEqual(
                getattr(new_people_search, keyData),
                valueData,
                f"Incorrect compare DATA on new object in [{keyData}] field: [{getattr(new_people_search, keyData)}]<>[{valueData}]"
            )

    result = api.get_people_search_locations(new_people_search)
    self.assertEqual(len(result), len(search_data['locations']), "Incorrect locations list length")

    for cur_search_location in result:
        self.assertEqual(
            cur_search_location.id_location in search_data['locations'],
            True,
            "Incorrect DATA save in locations"
        )

    return new_people_search


def sync_search(self: TestCase):
    pass
