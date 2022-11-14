from pullgerReflection.org__bbb import models


def add_country(id_iso, description, *args, **kwargs):
    return models.Country.add(id_iso=id_iso, description=description)


def get_country_by_iso(id_iso=None, id_iso_country=None, *args, **kwargs):
    if id_iso is not None:
        issue_id_iso = id_iso
    else:
        issue_id_iso = id_iso_country
    return models.Country.objects.get_by_keys(id_iso=issue_id_iso)