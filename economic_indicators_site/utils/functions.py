
# This function creates unique identifiers for raport separate fields
def identify(user_id, num_of_reports, time_period) -> str:
    return f'{user_id}.{num_of_reports}.{time_period}'
