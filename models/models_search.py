import uuid as uuid_class

from . import models_locations
from . import models_catgories
from . import models_profile

from django.db import models
from django.db.models import signals
from django.db.models import F
from django.dispatch import receiver

from pullgerInternalControl.pullgerReflection.logging import logger
from pullgerDataSynchronization import signal
#TDD
from pullgerDomain.org.bbb import search as pd_org_bbb_search
from . import models_search_tdd

from pullgerDevelopmentFramework import dynamic_code

from . import models_search_dm
RELOAD_SET = (models_search_dm, pd_org_bbb_search, models_search_tdd)


class SearchRequestsManager(models.Manager):
    def get_by_uuid(self, uuid: str, *args, **kwargs):
        return self.filter(uuid=uuid).first()

    def get_by_key(self, category, city):
        result_query = self.filter(category=category, city=city)\
            .select_related() \
            .annotate(
                id_name_category=F('category__id_name'),
                id_name_city=F('city__id_name'),
                id_iso_country=F('city__country__id_iso'),
                id_iso_state=F('city__state__id_iso')
            )

        if len(result_query) == 0:
            return None
        else:
            if len(result_query) > 1:
                logger.warning(
                    msg=f"DB corrupt (several records with category [{str(category)}] and city [{str(city)}])"
                )
            return result_query.first()


class SearchRequests(models.Model):
    class SearchScopes(models.TextChoices):
        PEOPLE = 'PEOPLE', 'people'

    uuid = models.UUIDField(default=uuid_class.uuid4, primary_key=True)

    category = models.ForeignKey(
        models_catgories.Category,
        verbose_name='uuid_category',
        db_column='uuid_category',
        to_field='uuid',
        on_delete=models.DO_NOTHING
    )

    city = models.ForeignKey(
        models_locations.City,
        verbose_name='uuid_city',
        db_column='uuid_city',
        to_field='uuid',
        on_delete=models.DO_NOTHING
    )

    # Send to customer
    sync_executed = models.BooleanField(blank=None, null=True)
    sync_status = models.IntegerField(null=True)

    moment_create = models.DateTimeField(auto_now_add=True, null=True)
    moment_update = models.DateTimeField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)

    page_loaded = models.IntegerField(null=True)
    page_count = models.IntegerField(null=True)

    updated = models.BooleanField(blank=False, null=True)
    # ---------------------------------
    objects = SearchRequestsManager()
    domain = pd_org_bbb_search.SearchDomain

    def to_json(self):
        return models_search_tdd.to_json(self)

    # @property
    # def domain(self):
    #     return pd_org_bbb_search.SearchDomain

    @property
    def db_table(self):
        return self._meta.db_table

    def get_results(self):
        return SearchRequestResult.objects.filter(search_request=self)

    @staticmethod
    def add(category, city):
        issue_element = SearchRequests.objects.get_by_key(category=category, city=city)
        if issue_element is None:
            issue_element = SearchRequests()
            issue_element.category = category
            issue_element.city = city
            issue_element.save()

        return issue_element

    def sync(self=None, data=None, session=None, **kwargs):
        dynamic_code.lib_reloader(RELOAD_SET)
        return models_search_dm.search_requests_sync(self, data=data, session=session, **kwargs)

    def pull_data(self, session):
        dynamic_code.lib_reloader(RELOAD_SET)
        domain = self.domain(session=session)
        domain.get(**self.to_json())
        pull_data = domain.pull()

        response = {
            "meta": {
                "page_loaded": pull_data.get("meta").get("page_loaded"),
                "page_count": pull_data.get("meta").get("page_count")
            },
            "related_list":
                {
                    "profiles": pull_data.get('elements')
                }
        }

        return response


class SearchRequestResultManager(models.Manager):
    def is_link_exist(self, profile):
        if len(self.filter(profile=profile)) > 0:
            return True
        else:
            return False


class SearchRequestResult(models.Model):
    uuid = models.UUIDField(default=uuid_class.uuid4, editable=False, primary_key=True)

    search_request = models.ForeignKey(
        SearchRequests,
        verbose_name='uuid_search_request',
        db_column='uuid_search_request',
        to_field='uuid',
        on_delete=models.CASCADE
    )
    profile = models.ForeignKey(
        models_profile.Profile,
        verbose_name='uuid_profile',
        db_column='uuid_profile',
        to_field='uuid',
        on_delete=models.CASCADE
    )

    objects = SearchRequestResultManager()

    @staticmethod
    def create_link(search_request, profile):
        if SearchRequestResult.objects.is_link_exist(profile) is False:
            new_search_request_result = SearchRequestResult()
            new_search_request_result.search_request = search_request
            new_search_request_result.profile = profile
            new_search_request_result.save()


@receiver(signals.post_save, sender=SearchRequests)
def add_taskflow_on_crating(sender, instance, created, **kwargs):
    signal.registrate_sync_task(created=created, instance=instance, sender=sender)
