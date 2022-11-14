from django.test import TestCase
from django.test import tag

from pullgerReflection.org__bbb.tests.tools import unitOperationsR


class Test000Locations(TestCase):
    @tag("PROD")
    def test_000_add_country(self):
        unitOperationsR.add_country(self)

    @tag("PROD")
    def test_001_add_state(self):
        unitOperationsR.add_state(self)

    @tag("PROD")
    def test_001_add_city(self):
        unitOperationsR.add_city(self)
