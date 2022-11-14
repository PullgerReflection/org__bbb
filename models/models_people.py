from datetime import date
import uuid

from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.db.models import Q

from pullgerDomain.com.linkedin import port as linkedinPORT
from pullgerFootPrint.com.linkedin import general as linkedinGENERAL
from pullgerInternalControl import pIC_pR
from pullgerInternalControl import pIC_pD
from pullgerInternalControl.pullgerReflection.Model.logging import logger

from .models_profile import Companies

from pullgerDomain.com.linkedin import port


class PeopleManager(models.Manager):
    def get_all_persons(self, **kwargs):
        if 'date_loaded' in kwargs:
            return self.filter(date_full_loaded=kwargs['date_loaded'])
        elif 'lte_date_loaded' in kwargs:
            return self.filter(date_full_loaded__lte=kwargs['lte_date_loaded'])
        elif 'ne_date_loaded' in kwargs:
            return self.filter(~Q(date_full_loaded=kwargs['ne_date_loaded']))
        elif 'eq_date_loaded' in kwargs:
            return self.filter(Q(date_full_loaded=kwargs['eq_date_loaded']))
        else:
            return People.objects.all()

    @staticmethod
    def get_by_uuid(uuid_element: str):
        return People.objects.filter(uuid=uuid_element).first()

    @staticmethod
    def get_people_by_uuid(uuid_people):
        res = People.objects.filter(uuid=uuid_people)[:1]
        if len(res) == 1:
            return res[0]
        else:
            return None

    @staticmethod
    def get_by_id(id_element):
        res = People.objects.filter(id=id_element)[:1]
        if len(res) == 1:
            return res[0]
        else:
            return None

    def is_exist(self, id_element: (str, int)) -> bool:
        if isinstance(id_element, int):
            identification = id_element
        elif isinstance(id_element, str):
            try:
                identification = int(id_element)
            except BaseException as e:
                pIC_pR.Model.IncorrectData(
                    msg=f"Incorrect type of id_people. [{str(e)}]",
                    level=30
                )
        else:
            pIC_pR.Model.IncorrectData(
                msg=f"Incorrect type of id_people. [{str(id_element)}]",
                level=30
            )

        filter_result = self.filter(id=identification)
        filter_result_count = len(filter_result)

        if filter_result_count == 0:
            return False
        else:
            if filter_result_count > 1:
                logger.warning(msg=f"People have id duplication [{id_element}]")
            return True


class People(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    id = models.IntegerField(blank=False, null=True)
    nick = models.CharField(max_length=150, null=True)

    first_name = models.CharField(max_length=150, null=True)
    second_name = models.CharField(max_length=150, null=True)
    full_name = models.CharField(max_length=300, null=True)

    url = models.CharField(max_length=300, null=True)
    description = models.CharField(max_length=300, null=True)

    location = models.CharField(max_length=300, null=True)

    date_small_loaded = models.DateField(null=True)
    date_full_loaded = models.DateField(null=True)

    objects = PeopleManager()
    domain = port.Domain

    def cleaningURL(self):
        self.url = linkedinPORT.PeopleSubject.getCleanedURL(self.url)

    def normalization(self):
        result = None
        if self.url is not None:
            # ==================================================
            urlClear = linkedinGENERAL.get_cleaned_url(self.url)
            if self.url != urlClear:
                self.url = urlClear
                result = True
            # ==================================================
            # ==================================================
            urlNICK = linkedinGENERAL.getNickFromURL(urlClear)
            # urlNICK = linkedinPORT.PeopleSubject.getNickFromURL(urlClear)
            if self.nick != urlNICK:
                self.nick = urlNICK
                result = True
            # ==================================================
        return result

    def get_domain(self, session):
        return session.domain.get_person(id_person=self.id, nick=self.nick)

    def update_full_load_data_people(self):
        self.date_full_loaded = date.today()
        try:
            self.save()
        except BaseException as e:
            raise pIC_pR.Model.Error(
                'Not enough parameters. Need "object="',
                level=50,
                exception=e
            )

    def sync(self=None, session=None, data=None):
        if self is None:
            if data is not None:
                self = People.save_data(data=data)
            else:
                pIC_pR.Model.Error(
                    msg=f"Empy variable DATA: [{str(e)}]",
                    level=50
                )
        else:
            if session is not None:
                pulled_data = self.pull_data(session=session)
                self.sync(data=pulled_data)
            elif data is not None:
                self.save_data(data=data)

        return self

    def save_data(self=None, data=None):
        if self is None:
            id_people = data.get('id')

            if id_people is not None:
                is_people_exist = People.objects.is_exist(id_people)

            if is_people_exist is False:
                self = People()
            else:
                self = People.objects.get_by_id(id_people)

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

        try:
            self.save()
        except Exception as e:
            pIC_pR.Model.Error(
                msg=f"Unexpected error on save People: [{str(e)}]"
            )

        if 'people_experience' in data:
            experience_list = data.get('people_experience')

            if experience_list != 0:
                People_Experience.objects.del_experiences(uuid=self.uuid)

                errors_in_loop = False

                for cur_experience in experience_list:
                    if cur_experience['companyID'] is not None or cur_experience['companyNICK'] is not None:
                        newCompanyDict = {
                            "id": cur_experience['companyID'],
                            "nick": cur_experience['companyNICK'],
                            "name": cur_experience['companyName'],
                            "searcher": "NEO",
                            "url": cur_experience['companyURL']
                        }
                        newCompany = Companies.add_company(**newCompanyDict)

                        newPeopleExperienceDict = {
                            "job_description": cur_experience['job_description'],
                            "job_timing_type": cur_experience['job_timing_type']
                        }

                        res_add_experience = People_Experience.add_people_experience(
                            people=self, company=newCompany, **newPeopleExperienceDict)

                        if res_add_experience is None:
                            errors_in_loop = True
                if errors_in_loop is False:
                    self.update_full_load_data_people()
        return self

    def pull_data(self, session: object) -> list:
        import time

        person_domain = self.get_domain(session)
        if person_domain is None:
            raise pIC_pD.pages.General(
                msg="Error on page loading.",
                level=50
            )
        else:
            response = {
                     'meta': {
                     },
                     'people_experience': []
                }

            list_of_experience = person_domain.get_list_of_experience()

            for cur_experience in list_of_experience:
                response['people_experience'].append(cur_experience)

            return response

        # experience_list = self._object.DomainObject.get_list_of_experience()

        # import time
        #
        # session.domain.search(self.search_scope.lower(), self.get_locations_list(), self.keywords)
        # count_results = session.domain.get_count_of_results()
        #
        # response = {
        #     'meta': {
        #         'count_results': count_results
        #     },
        #     'elements': []
        # }
        #
        # EndOfSearch = False
        #
        # while EndOfSearch is False:
        #     time.sleep(4)
        #     listOfPersons = session.domain.getListOfPeoples()
        #     for elOfList in listOfPersons:
        #         response['elements'].append(elOfList)
        #
        #     if session.domain.listOfPeopleNext() is not True:
        #         EndOfSearch = True
        #
        # return response


people = People


@receiver(signals.pre_save, sender=People)
def add_people_uuid(sender, instance, **kwargs):
    import uuid

    if not instance.uuid:
        instance.uuid = str(uuid.uuid1())


class People_ExperienceManager(models.Manager):
    @staticmethod
    def delExperiencesIntrnel(inPeople):
        rowsExperiences = people_experience.objects.filter(people=inPeople.uuid)
        for rowExperiences in rowsExperiences:
            rowExperiences.delete()

    @staticmethod
    def del_experiences(uuid: str = None, id: int = None, people = None):
        if uuid is not None:
            result = People_ExperienceManager._del_experiences_internal(PeopleManager.get_by_uuid(uuid))
        elif id is not None:
            result = People_ExperienceManager._del_experiences_internal(PeopleManager.get_by_uuid(id))
        elif people is not None:
            result = People_ExperienceManager._del_experiences_internal(people)
        return result

    @staticmethod
    def _del_experiences_internal(people):
        rows_experiences = People_Experience.objects.filter(people=people)
        for row_experiences in rows_experiences:
            row_experiences.delete()


class People_Experience(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    people = models.ForeignKey(
        People,
        verbose_name='uuid_people',
        db_column='uuid_people',
        to_field='uuid',
        on_delete=models.CASCADE)
    companies = models.ForeignKey(
        Companies,
        verbose_name='uuid_companies',
        db_column='uuid_companies',
        to_field='uuid',
        on_delete=models.CASCADE
    )
    job_description = models.CharField(max_length=300, null=True)
    job_timing_type = models.CharField(max_length=50, null=True)
    date_small_loaded = models.DateField(null=True)

    objects = People_ExperienceManager()

    @staticmethod
    def add_people_experience(people, company, **kwargs):
        result_add = None

        createPeopleExperience = People_Experience()

        for key, value in kwargs.items():
            if hasattr(createPeopleExperience, key):
                setattr(createPeopleExperience, key, value)
        try:
            createPeopleExperience.people = people
            createPeopleExperience.companies = company
            createPeopleExperience.save()
            result_add = createPeopleExperience
        except BaseException as e:
            raise pIC_pR.Model.Error(
                f"Incorrect creating company: {str(kwargs)}",
                exception=e
            )

        return result_add


people_experience = People_Experience
