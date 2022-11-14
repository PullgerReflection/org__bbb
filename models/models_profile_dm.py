from pullgerReflection.org__bbb import models

from pullgerInternalControl.pullgerReflection import Model as ModelExceptions
from pullgerInternalControl import pIC_pR


def profile_sync(self: "models.Profile",
                 data,
                 session,
                 **kwargs):

    if self is None:
        if data is not None:
            self = models.Profile.save_data(data=data)
        else:
            pIC_pR.Model.Error(
                msg=f"Empy variable DATA: [{str(data)}]",
                level=50
            )
    else:
        if data is not None:
            element = data.get('element')
            # for cur_element in elements:
            #     with transaction.atomic():
            #         profile_element = models_profile.Profile.sync(data=cur_element)
            #         SearchRequestResult.create_link(self, profile_element)
        elif session is not None:
            pulled_data = self.pull_data(session)
            self.sync(data=pulled_data)
        else:
            ModelExceptions.IncorrectData(
                msg="Incorrect function parameters.",
                level=40
            )
    return self


def profile_save_data(self: "models.Profile",
                      data,
                      **kwargs):
    if self is None:
        element_data = data.get('element')
        id_name_issue = element_data.get('id_name_profile')
        if id_name_issue is None:
            id_name_issue = element_data.get('id_name')

        if id_name_issue is not None:
            is_profile_exist = models.Profile.objects.is_exist(id_name=id_name_issue)
        else:
            pIC_pR.Model.IncorrectData(
                msg="No 'id_name_profile' field",
                level=40
            )

        if is_profile_exist is False:
            self = models.Profile()
        else:
            self = models.Profile.objects.get_by_keys(id_name_issue)

    self.id_name = id_name_issue

    id_iso_country = element_data.get('id_iso_country')
    id_iso_state = element_data.get('id_iso_state')
    id_name_city = element_data.get('id_name_city')

    city = models.City.objects.get_by_keys(
        id_iso_country=id_iso_country,
        id_iso_state=id_iso_state,
        id_name_city=id_name_city,
        force=True
    )

    self.city = city

    for key, value in element_data.items():
        if hasattr(self, key):
            setattr(self, key, value)

    try:
        self.save()
    except Exception as e:
        pIC_pR.Model.Error(
            msg=f"Unexpected error on save People: [{str(e)}]"
        )

    return self


def profile_complaints_reg_sync(self: "models.Profile",
                                data,
                                session,
                                **kwargs):

    if self is None:
        if data is not None:
            self = models.Profile.save_data(data=data)
        else:
            pIC_pR.Model.Error(
                msg=f"Empy variable DATA: [{str(data)}]",
                level=50
            )
    else:
        if data is not None:
            element = data.get('element')
            # for cur_element in elements:
            #     with transaction.atomic():
            #         profile_element = models_profile.Profile.sync(data=cur_element)
            #         SearchRequestResult.create_link(self, profile_element)
        elif session is not None:
            pulled_data = self.pull_data(session)
            self.sync(data=pulled_data)
        else:
            ModelExceptions.IncorrectData(
                msg="Incorrect function parameters.",
                level=40
            )
    return self


def profile_complaints_reg_save_data(self: "models.Profile",
                                     data,
                                     **kwargs):
    if self is None:
        element_data = data.get('element')
        id_name_profile = element_data.get('id_name_profile')

        if id_name_profile is not None:
            is_profile_exist = models.Profile.objects.is_exist(id_name=id_name_profile)
        else:
            pIC_pR.Model.IncorrectData(
                msg="No 'id_name_profile' field",
                level=40
            )

        if is_profile_exist is False:
            self = models.Profile()
        else:
            self = models.Profile().objects.get_by_keys(id_name_profile)

    for key, value in element_data.items():
        if hasattr(self, key):
            setattr(self, key, value)

    try:
        self.save()
    except Exception as e:
        pIC_pR.Model.Error(
            msg=f"Unexpected error on save People: [{str(e)}]"
        )

    return self

