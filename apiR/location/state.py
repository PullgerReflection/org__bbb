from pullgerReflection.org__bbb import models


def add_state(*args, **kwargs):
    return models.State.add(*args, **kwargs)


def get_state_by_iso(*args, **kwargs):
    return models.State.objects.get_by_keys(*args, **kwargs)
