from django.test import TestCase

from pullgerReflection.org__bbb import apiR
from pullgerReflection.org__bbb.models import models_catgories
from pullgerReflection.org__bbb.models import models_locations
from pullgerReflection.org__bbb.models import models_search
from pullgerReflection.org__bbb.tests.tools import dataTemplatesR

from pullgerDataSynchronization import apiDS


def add_search_request(self: TestCase):

    data_elements_list = dataTemplatesR.search_request_data()
    for data_element in data_elements_list:
        issue_city = apiR.get_city_by_id_name(**data_element)
        self.assertIsInstance(issue_city, models_locations.City, "Incorrect return get 'City'")
        
        issue_category = apiR.get_category_by_id_name(**data_element)
        self.assertIsInstance(issue_category, models_catgories.Category, "Incorrect return on get 'Category'")

        issue_element = apiR.add_search_request(city=issue_city, category=issue_category)
        self.assertIsInstance(issue_element, models_search.SearchRequests, "Incorrect return on get 'Category'")

        issue_search_request = apiR.get_search_request_by_ids(**data_element)

        for (key, value) in data_element.items():
            self.assertEqual(getattr(issue_search_request, key), value, "Incorrect compare DATA in new 'search request'")

    return issue_element


def add_search_request_all(self: TestCase):
    city_count = apiR.get_city_count()
    category_count = apiR.get_category_count()
    estimated_quantity = city_count*category_count

    search_requests_created = apiR.accordance_search_requests()
    self.assertEqual(search_requests_created, estimated_quantity, "Incorrect number of elements created.")

    task_for_execution = apiDS.get_all_count()
    self.assertEqual(task_for_execution, estimated_quantity, "Incorrect number task to execution.")
