import uuid as uuid_class

from django.db import models
from django.db.models import signals
from django.db.models import Q
from django.db.models import F
from django.dispatch import receiver

from pullgerInternalControl import pIC_pR
from pullgerInternalControl.pullgerReflection.Model.logging import logger

from pullgerReflection.org__bbb.models import models_locations


class CountryManagers(models.Manager):

    def get_all(self):
        return self.all()

    def get_by_keys(self,
                    id_iso: str = None,
                    id_iso_country: str = None,
                    force: bool = False,
                    *args,
                    **kwargs
                    ) -> "Country":
        if id_iso_country is not None:
            id_iso_issue = id_iso_country
        else:
            id_iso_issue = id_iso

        if id_iso_issue is not None:
            result_query = self.filter(id_iso=id_iso_issue)
            if len(result_query) == 0:
                if force is True:
                    return Country.add(id_iso_issue)
                else:
                    return None
            else:
                if len(result_query) > 1:
                    logger.warning(
                        msg=f"DB corrupt (several records with id_iso [{str(id_iso_issue)}])"
                    )
                return result_query.first()
            pIC_pR.Model.General(
                msg="Unexpected code position.",
                level=30
            )
        else:
            pIC_pR.Model.IncorrectData(
                msg="No field 'id_iso/id_iso_country.'",
                level=30
            )


class Country(models.Model):

    uuid = models.UUIDField(default=uuid_class.uuid4, editable=False, primary_key=True)
    id_iso = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)

    # Registration change
    moment_create = models.DateField(auto_now_add=True, null=True)
    moment_update = models.DateField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    # ---------------------------------------------------------------------
    objects = CountryManagers()

    # ---------------------------------------------------------------------

    @staticmethod
    def add(id_iso: str, description: str = None, **kwargs):
        if id_iso is not None:
            element = Country.objects.get_by_keys(id_iso)

            if element is None:
                new_element = Country()
                new_element.id_iso = id_iso
                if description is not None:
                    new_element.description = description
                else:
                    new_element.description = ""
                new_element.save()
            else:
                new_element = element

            return new_element
        else:
            pIC_pR.Model.IncorrectData(
                msg="No required data in request",
                level=30
            )

    # def to_json(self):
    #     return(
    #         str({
    #             "uuid": str(self.uuid),
    #             "id_location": self.id_location,
    #             "description": self.description
    #         })
    #     )


class StateManagers(models.Manager):

    def get_all(self):
        return self.all()

    def get_by_keys(self,
                    id_iso: str = None,
                    id_iso_state: str = None,
                    country: Country = None,
                    force: bool = False,
                    *args,
                    **kwargs
                    ) -> "State":
        if id_iso_state is not None:
            id_iso_issue = id_iso_state
        else:
            id_iso_issue = id_iso

        if id_iso_issue is not None:
            result_query = self.filter(id_iso=id_iso_issue, country=country)\
                .select_related('country')\
                .annotate(id_iso_country=F('country__id_iso'))

            if len(result_query) == 0:
                if force is True:
                    return State.add(id_iso=id_iso_issue, country=country)
                else:
                    return None
            else:
                if len(result_query) > 1:
                    logger.warning(
                        msg=f"DB corrupt (several records with id_iso [{str(id_iso_issue)}])"
                    )
                return result_query.first()

            pIC_pR.Model.General(
                msg="Algorithm error. Unexpected position.",
                level=50
            )
        else:
            pIC_pR.Model.IncorrectData(
                msg="Incorrect 'id_iso/id_iso_state'",
                level=30
            )


class State(models.Model):

    uuid = models.UUIDField(default=uuid_class.uuid4, editable=False, primary_key=True)
    id_iso = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    country = models.ForeignKey(
        Country,
        verbose_name='uuid_country',
        db_column='uuid_country',
        to_field='uuid',
        on_delete=models.CASCADE
    )

    # Registration change
    moment_create = models.DateField(auto_now_add=True, null=True)
    moment_update = models.DateField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    # ---------------------------------------------------------------------
    objects = StateManagers()

    # ---------------------------------------------------------------------

    @staticmethod
    def add(id_iso: str = None, id_iso_state: str = None, country = None, description: str = None, *args, **kwargs):
        if id_iso_state is not None:
            id_iso_issue = id_iso_state
        else:
            id_iso_issue = id_iso

        if id_iso_issue is not None:
            issue_element = State.objects.get_by_keys(id_iso_state=id_iso_issue, country=country)

            if issue_element is None:
                issue_element = State()
                issue_element.id_iso = id_iso_issue
                if description is not None:
                    issue_element.description = description
                else:
                    issue_element.description = ""
                issue_element.country = country
                issue_element.save()

            return issue_element
        else:
            pIC_pR.Model.IncorrectData(
                msg="No required data in request. 'id_iso/id_iso_state'",
                level=30
            )


class CityManager(models.Manager):

    def get_count(self):
        return self.all().count()

    def get_all(self):
        return self.all()

    def get_by_keys(self,
                    state=None,
                    id_iso_state=None,
                    country=None,
                    id_iso_country=None,
                    id_name: str = None,
                    id_name_city: str = None,
                    force: bool = False
                    ) -> "City":
        if id_name_city is not None:
            id_name_issue = id_name_city
        else:
            id_name_issue = id_name

        if id_name_issue is not None:
            if country is None:
                if id_iso_country is not None:
                    country = Country.objects.get_by_keys(id_iso_country=id_iso_country, force=force)
                else:
                    pIC_pR.Model.IncorrectData(
                        msg=f"No data in fields 'country/id_iso_country'",
                        level=40
                    )
            if state is None:
                if id_iso_state is not None:
                    state = State.objects.get_by_keys(
                        id_iso_state=id_iso_state,
                        country=country,
                        force=force
                    )
                else:
                    pIC_pR.Model.IncorrectData(
                        msg=f"No data in fields 'state/id_iso_state'",
                        level=40
                    )

            filters = {
                "id_name": id_name_issue
            }
            if state is not None:
                filters["state"] = state
            if country is not None:
                filters["country"] = country

            result_query = self.filter(**filters)\
                .select_related() \
                .annotate(id_iso_country=F('country__id_iso'), id_iso_state=F('state__id_iso'))

            if len(result_query) == 0:
                if force is True:
                    return City.add(
                        country=country,
                        state=state,
                        id_name=filters['id_name'],
                    )
                else:
                    return None
            else:
                if len(result_query) > 1:
                    if state is not None and country is not None:
                        logger.warning(
                            msg=f"DB corrupt (several records with id_iso [{str(id_name)}])"
                        )
                    return result_query.first
                else:
                    return result_query.first()
        else:
            pIC_pR.Model.IncorrectData(
                msg="Incorrect input data.",
                level=40
            )


class City(models.Model):

    uuid = models.UUIDField(default=uuid_class.uuid4, editable=False, primary_key=True)
    id_name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    country = models.ForeignKey(
        Country,
        verbose_name='uuid_country',
        db_column='uuid_country',
        to_field='uuid',
        null=False,
        on_delete=models.DO_NOTHING
    )
    state = models.ForeignKey(
        State,
        verbose_name='uuid_state',
        db_column='uuid_state',
        to_field='uuid',
        null=False,
        on_delete=models.DO_NOTHING
    )

    # Registration change
    moment_create = models.DateField(auto_now_add=True, null=True)
    moment_update = models.DateField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    # ---------------------------------------------------------------------
    objects = CityManager()

    # ---------------------------------------------------------------------

    @staticmethod
    def add(country, state, description: str = None, id_name: str = None, id_name_city: str = None, **kwargs):
        if id_name_city is not None:
            id_name_issue = id_name_city
        else:
            id_name_issue = id_name

        if id_name_issue is not None:
            element = City.objects.get_by_keys(state=state, country=country, id_name=id_name_issue)

            if element is None:
                new_element = City()
                new_element.id_name = id_name_issue
                if description is not None:
                    new_element.description = description
                else:
                    new_element.description = ""
                new_element.country = country
                new_element.state = state
                new_element.save()
            else:
                new_element = element

            return new_element
        else:
            pIC_pR.Model.IncorrectData(
                msg="No required data in request",
                level=30
            )
