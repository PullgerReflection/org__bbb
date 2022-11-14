import uuid as uuid_class

from django.db import models
from django.db.models import signals
from django.db.models import Q
from django.db.models import F
from django.dispatch import receiver

from pullgerInternalControl.pullgerReflection import Model as ModelExceptions
from pullgerInternalControl.pullgerReflection.Model.logging import logger


class CategoryManager(models.Manager):

    def get_count(self):
        return self.all().count()

    def get_all(self):
        return self.all()

    def get_by_keys(self, id_name: str) -> "Category":
        result_query = self.filter(id_name=id_name)
        if len(result_query) == 0:
            return None
        else:
            if len(result_query) > 1:
                logger.warning(
                    msg=f"DB corrupt (several records with id_iso [{str(id_name)}])"
                )
            return result_query.first()


class Category(models.Model):

    uuid = models.UUIDField(default=uuid_class.uuid4, editable=False, primary_key=True)
    id_name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)

    # Registration change
    moment_create = models.DateField(auto_now_add=True, null=True)
    moment_update = models.DateField(auto_now=True, null=True)
    moment_sync = models.DateTimeField(null=True)
    # ---------------------------------------------------------------------
    objects = CategoryManager()

    # ---------------------------------------------------------------------

    @staticmethod
    def add(id_name_category: str = None, id_name: str = None, description: str = None, **kwargs):
        if id_name_category is not None:
            id_name_issue = id_name_category
        else:
            id_name_issue = id_name

        if id_name_issue is not None:
            issue_element = Category.objects.get_by_keys(id_name=id_name_issue)

            if issue_element is None:
                issue_element = Category()
                issue_element.id_name = id_name_issue
                if description is not None:
                    issue_element.description = description
                else:
                    issue_element.description = ""
                issue_element.save()
            else:
                issue_element = issue_element

            return issue_element
        else:
            ModelExceptions.IncorrectData(
                msg="No required data in request",
                level=30
            )
