# This function creates unique identifiers for raport separate fields
from django.db.models import Model


def identify(user_id, num_of_reports, time_period) -> str:
    return f'{user_id}.{num_of_reports}.{time_period}'


def clearify(data_model, identifier: str):
    try:
        model = data_model.objects.get(identifier=identifier)
        data_model.delete(model)
    except:
        return
