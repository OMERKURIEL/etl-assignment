from datetime import datetime
import json


def remove_sensitive_fields(data):
    """
    Remove keys starting with '_' from the JSON object recursively.

    :param data: JSON-like object (dict or list).
    :return: The same structure with sensitive fields removed.
    """
    if isinstance(data, dict):
        cleaned_data = {}
        for key, value in data.items():
            if not key.startswith('_'):
                cleaned_data[key] = remove_sensitive_fields(value)
            return cleaned_data
    elif isinstance(data, list):
        return [remove_sensitive_fields(item) for item in data]
    else:
        return data

def validate_fields_length(data):
    """
    Validate that all string fields in the JSON are ≤ 64 characters.

    :param data: JSON-like object (dict or list).
    :raises ValueError: If any string field exceeds 64 characters.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            validate_fields_length(value)
    elif isinstance(data, list):
        for item in data:
            validate_fields_length(item)
    elif isinstance(data, str):
        if len(data) > 64:
            raise ValueError(f"String '{data}' exceeds 64 characters.")


def validate_dates(data):
    """
    Validate that all dates in the JSON are within the range 2014-01-01 to 2024-12-31.

    :param data: JSON-like object (dict or list).
    :raises ValueError: If any date is out of range.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            validate_dates(value)

    elif isinstance(data, list):
        for date in data:
            validate_dates(date)

    elif isinstance(data, str):
        try:
            # Try parsing the string as a date
            date = datetime.strptime(data, "%Y-%m-%d")
            if not (datetime(2014, 1, 1) <= date <= datetime(2024, 12, 31)):
                raise ValueError(f"Date '{data}' is out of range.")
        except ValueError:
            # Ignore strings that aren't valid dates
            pass



def validate_participants_age(data):
    """
    Validate that the participant is at least 40 years old.

    :param data: JSON-like object (dict).
    :raises ValueError: If the participant's age is < 40.
    """
    if "individual_metadata" in data and "date_of_birth" in data["individual_metadata"]:
        date_of_birth = datetime.strptime(data["individual_metadata"]["date_of_birth"], "%Y-%m-%d")
        participants_age = (datetime.now() - date_of_birth) // 365
        if participants_age < 40:
            raise ValueError(f"Participant's age '{participants_age}' is less than 40 years old.")
    else:
        raise ValueError("Missing 'individual_metadata' or 'date_of_birth'")



