from django.test import TestCase
from django.test import tag

from pullgerReflection.org__bbb.tests.tools import unitOperationsR


class Test000Locations(TestCase):
    @tag("PROD")
    def test_000_add_category(self):
        unitOperationsR.add_category(self)
