import os
from rest_framework.test import APITestCase

from pullgerDevelopmentFramework import nocode

from django.test import tag


class Test000NoCode(APITestCase):
    @tag('--NoCode--')
    def test_no_code(self):
        nocode.executor(self=self, file=__file__)
