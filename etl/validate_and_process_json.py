from datetime import datetime
import json
import logging


def remove_sensitive_fields(data):
    """
    Remove keys starting with '_' from the JSON object recursively.

    :param data: JSON-like object (dict or list).
    :return: The same structure with sensitive fields removed.
    """
    if isinstance(data, dict):
        return {
            key: remove_sensitive_fields(value)
            for key, value in data.items()
            if not key.startswith('_')
        }

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
            logging.error(f"String '{data}' exceeds 64 characters")
            raise ValueError(f"String '{data}' exceeds 64 characters.")



def validate_dates(data, start_date=None, end_date=None, date_fields=None):
    """
    Validate that all dates in the JSON are within the range 2014-01-01 to 2024-12-31.

    :param data: JSON-like object (dict or list).
    :param end_date: The earliest valid date (datetime object).
    :param start_date: The latest valid date (datetime object).
    :param date_fields: A set of fields expected to contain date values.
    :raises ValueError: If any date is out of range.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if key in date_fields and isinstance(value, str):
                try:
                    # Parse and validate the date
                    date = datetime.strptime(value, "%Y-%m-%d")
                    if not start_date <= date <= end_date:  # Raise an error if the field is out of the expected range
                        logging.error(f"Date '{value}' in field '{key}' is out of range.")
                        raise ValueError(f"Date '{value}' in field '{key}' is out of range.")

                except ValueError as e:
                    if "does not match format" in str(e): # Raise an error if date is not in the expected format
                        logging.error(f"invalid date format for field '{key}': {value}. Expected 'YYYY-MM-DD'.")
                        raise ValueError(f"Invalid date format for field '{key}': '{value}'. Expected 'YYYY-MM-DD'.")
                    else:
                        raise
            elif isinstance(value, (dict, list)): # Recursively validate nested structures
                validate_dates(value, start_date, end_date, date_fields)
    elif isinstance(data, list):
        for item in data:
            validate_dates(item, start_date, end_date, date_fields)



def validate_participants_age(data):
    """
    Validate that the participant is at least 40 years old.

    :param data: JSON-like object (dict).
    :raises ValueError: If the participant's age is < 40.
    """
    if "individual_metadata" in data and "date_of_birth" in data["individual_metadata"]:
        try:
            date_of_birth = datetime.strptime(data["individual_metadata"]["date_of_birth"], "%Y-%m-%d")
            participants_age = (datetime.now() - date_of_birth).days // 365
            if participants_age < 40:
                logging.error(f"Participant's age '{participants_age}' is less than 40 years old.")
                raise ValueError(f"Participant's age '{participants_age}' is less than 40 years old.")
        except Exception:
            raise

    else:
        logging.error(f"Missing 'individual_metadata' or 'date_of_birth' field.")
        raise ValueError("Missing 'individual_metadata' or 'date_of_birth'")



def process_json_files(json_file_path):
    """
    Validate and clean metadata in the .json file.

    :param json_file_path: Path to the .json file.
    :return: Cleansed metadata.
    """
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    try:
        logging.info(f"Validating JSON file: {json_file_path}")

        logging.debug("Validating fields length")
        validate_fields_length(data)

        start_date = datetime(2014, 1, 1)
        end_date = datetime(2024, 12, 31)
        date_fields = {"date_requested", "date_completed", "collection_date"}
        logging.debug("Validating dates.")
        validate_dates(data, start_date, end_date, date_fields)

        logging.debug("Validating participant's age.")
        validate_participants_age(data)

    except Exception as e:
        raise

    data = remove_sensitive_fields(data)
    logging.info("JSON file validation and processing complete.")
    return data








