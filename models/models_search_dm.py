
# Django library
from django.db import transaction

from pullgerReflection.org__bbb import models
from pullgerInternalControl.pullgerReflection import Model as ModelExceptions


def search_requests_sync(self: 'models.SearchRequests', data, session):
    if self is None:
        pass
    else:
        if data is not None:
            meta = data.get('meta')
            elements = data.get('related_list').get('profiles')
            with transaction.atomic():
                self.page_loaded = meta.get('page_loaded')
                self.page_count = meta.get('page_count')
                self.save()

                for cur_element in elements:
                    profile_element = models.Profile.sync(data={"element": cur_element})
                    models.ProfileComplaintsReg.add(profile=profile_element)
                    models.ProfileCustomerReviewsReg.add(profile=profile_element)
                    models.SearchRequestResult.create_link(self, profile_element)
        elif session is not None:
            pulled_data = self.pull_data(session)
            self.sync(data=pulled_data)
        else:
            ModelExceptions.IncorrectData(
                msg="Incorrect function parameters.",
                level=40
            )
    return self
