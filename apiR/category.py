from pullgerReflection.org__bbb import models


def add_category(id_name, description, *args, **kwargs):
    return models.Category.add(id_name=id_name, description=description)


def get_category_by_id_name(id_name=None, id_name_category=None, *args, **kwargs):
    if id_name is not None:
        issue_id_name = id_name
    else:
        issue_id_name = id_name_category

    return models.Category.objects.get_by_keys(id_name=issue_id_name)


def get_category_count():
    return models.Category.objects.get_count()


def get_category_all():
    return models.Category.objects.get_all()
