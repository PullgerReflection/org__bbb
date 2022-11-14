import uuid as uuid_class

from django.db import models

from pullgerInternalControl.pullgerReflection.Model.logging import logger

from pullgerDevelopmentFramework import dynamic_code

from pullgerReflection.org__bbb.models import models_locations
from . import models_profile_dm
RELOAD_SET = (models_profile_dm,)


class ProfileManager(models.Manager):
    testVar = None

    def is_exist(self, id_name: str = None, id_name_profile: str = None) -> bool:
        if id_name is not None:
            id_name_issue = id_name
        else:
            id_name_issue = id_name_profile

        filter_result = self.filter(id_name=id_name_issue)
        filter_result_count = len(filter_result)

        if filter_result_count == 0:
            return False
        else:
            if filter_result_count > 1:
                logger.warning(msg=f"Companies have id duplication [{id_name_issue}]")
            return True

    def get_by_keys(self, id_name: int):
        filter_result = self.filter(id_name=id_name)
        filter_result_count = len(filter_result)

        if filter_result_count == 0:
            return None
        else:
            if filter_result_count > 1:
                logger.warning(msg=f"Profile have id_name duplication [{id_name}]")
            return filter_result.first()

    def get_by_uuid(self, uuid: str):
        return self.filter(uuid=uuid).first()


class Profile(models.Model):
    uuid = models.UUIDField(default=uuid_class.uuid4, primary_key=True)
    id_name = models.CharField(max_length=100, null=True)
    city = models.ForeignKey(
        models_locations.City,
        verbose_name='uuid_city',
        db_column='uuid_city',
        to_field='uuid',
        on_delete=models.DO_NOTHING
    )

    moment_create = models.DateTimeField(auto_now_add=True, null=True)
    moment_update = models.DateTimeField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    updated = models.BooleanField(blank=False, null=True)

    objects = ProfileManager()

    def sync(self=None, data=None, session=None, **kwargs):
        dynamic_code.lib_reloader(RELOAD_SET)
        return models_profile_dm.profile_sync(self, data=data, session=session, **kwargs)

    def save_data(self=None, data=None, **kwargs):
        dynamic_code.lib_reloader(RELOAD_SET)
        return models_profile_dm.profile_save_data(self, data=data, **kwargs)

    # card_type = models.CharField(choices = CHOICES_CARD_TYPE, max_length=100, null=True)
    #
    # description = models.CharField(max_length=300, null=True)
    # overview = models.TextField(null=True)
    #
    # account_closed = models.BooleanField(blank=False, null=True)
    # incorrect_load = models.BooleanField(blank=False, null=True)
    #
    # url = models.CharField(max_length=300, null=True)
    # url_company = models.CharField(max_length=300, null=True)
    #
    # industry = models.CharField(max_length=300, null=True)
    #
    # company_size = models.CharField(max_length=300, null=True)
    # employee_linkedin = models.CharField(max_length=300, null=True)
    # followers = models.IntegerField(blank=False, null=True)
    #
    # countryISO = models.CharField(max_length=3, null=True)
    # location = models.CharField(max_length=300, null=True)
    # locationNameGeneral = models.CharField(max_length=300, null=True)
    #
    # headquarter = models.CharField(max_length=300, null=True)
    # founded = models.IntegerField(blank=False, null=True)
    #
    # searcher = models.CharField(max_length=100, null=True)
    #
    # date_small_loaded = models.DateField(null=True)
    # date_full_loaded = models.DateField(null=True)
    #
    # # Revenue
    # dnb_exist = models.BooleanField(blank=False, null=True)
    # dnb_revenue = models.BigIntegerField(blank=False, null=True)
    # dnb_profile = models.CharField(max_length=300, null=True)
    # dnb_employee = models.IntegerField(blank=False, null=True)
    #
    # # Outsource company
    # outsource_industry = models.BooleanField(blank=False, null=True)
    #
    # # Send to customer
    # sendToCustomer = models.DateField(null=True)
    # complies_parameters = models.BooleanField(blank=False, null=True)
    #


class ProfileComplaintsRegManager(models.Manager):
    def get_by_key(self, profile: 'ProfileComplaintsReg'):
        filter_result = self.filter(profile=profile)
        filter_result_count = len(filter_result)

        if filter_result_count == 0:
            return None
        else:
            if filter_result_count > 1:
                logger.warning(msg=f"Profile have id_name duplication [{str(profile)}]")
            return filter_result.first()

    def is_exist(self, profile):
        if len(self.filter(prifile=profile)) == 0:
            return False
        else:
            return True


class ProfileComplaintsReg(models.Model):
    uuid = models.UUIDField(default=uuid_class.uuid4, primary_key=True)
    profile = models.ForeignKey(
        Profile,
        verbose_name='uuid_profile',
        db_column='uuid_profile',
        to_field='uuid',
        on_delete=models.CASCADE
    )

    moment_create = models.DateTimeField(auto_now_add=True, null=True)
    moment_update = models.DateTimeField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    updated = models.BooleanField(blank=False, null=True)

    objects = ProfileComplaintsRegManager()

    @staticmethod
    def add(profile):
        issue_element = ProfileComplaintsReg.objects.get_by_key(profile)
        if issue_element is None:
            issue_element = ProfileComplaintsReg()
            issue_element.profile = profile
            issue_element.save()
        return issue_element

    def sync(self=None, data=None, session=None, **kwargs):
        dynamic_code.lib_reloader(RELOAD_SET)
        return models_profile_dm.profile_complaints_reg_sync(self, data=data, session=session, **kwargs)

    def save_data(self=None, data=None, **kwargs):
        dynamic_code.lib_reloader(RELOAD_SET)
        return models_profile_dm.rofile_complaints_reg_save_data(self, data=data, **kwargs)


class ProfileCustomerReviewsRegManager(models.Manager):
    def get_by_key(self, profile: 'ProfileComplaintsReg'):
        filter_result = self.filter(profile=profile)
        filter_result_count = len(filter_result)

        if filter_result_count == 0:
            return None
        else:
            if filter_result_count > 1:
                logger.warning(msg=f"Profile have id_name duplication [{str(profile)}]")

            return filter_result.first()

    def is_exist(self, profile):
        if len(self.filter(prifile=profile)) == 0:
            return False
        else:
            return True


class ProfileCustomerReviewsReg(models.Model):
    uuid = models.UUIDField(default=uuid_class.uuid4, primary_key=True)
    profile = models.ForeignKey(
        Profile,
        verbose_name='uuid_profile',
        db_column='uuid_profile',
        to_field='uuid',
        on_delete=models.CASCADE
    )

    moment_create = models.DateTimeField(auto_now_add=True, null=True)
    moment_update = models.DateTimeField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    updated = models.BooleanField(blank=False, null=True)

    objects = ProfileCustomerReviewsRegManager()

    @staticmethod
    def add(profile):
        issue_element = ProfileCustomerReviewsReg.objects.get_by_key(profile)
        if issue_element is None:
            issue_element = ProfileCustomerReviewsReg()
            issue_element.profile = profile
            issue_element.save()
        return issue_element

    def sync(self=None, data=None, session=None, **kwargs):
        dynamic_code.lib_reloader(RELOAD_SET)
        return models_profile_dm.profile_complaints_reg_sync(self, data=data, session=session, **kwargs)

    def save_data(self=None, data=None, **kwargs):
        dynamic_code.lib_reloader(RELOAD_SET)
        return models_profile_dm.rofile_complaints_reg_save_data(self, data=data, **kwargs)

