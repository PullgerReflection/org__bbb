from django.test import TestCase
from pullgerReflection.org__bbb.models import models_catgories
from pullgerReflection.org__bbb import apiR
from pullgerReflection.org__bbb.tests.tools import dataTemplatesR


def add_category(self: TestCase):

    data_elements_list = dataTemplatesR.category_data()
    for data_element in data_elements_list:
        new_element = apiR.add_category(**data_element)
        self.assertIsInstance(new_element, models_catgories.Category, "Incorrect return on create")

        issue_element = apiR.get_category_by_id_name(**data_element)

        for (key, value) in data_element.items():
            self.assertEqual(getattr(issue_element, key), value, "Incorrect compare DATA in new object")
