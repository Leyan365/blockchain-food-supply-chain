from datetime import datetime


EMAIL_LIKE_FIELDS = {'recipient', 'next_recipient'}


def clean_text(value):
    return (value or '').strip()


def validate_required_fields(form_data, field_labels):
    errors = []
    cleaned = {}

    for field, label in field_labels.items():
        value = clean_text(form_data.get(field))
        cleaned[field] = value
        if not value:
            errors.append(f"{label} is required.")

    return cleaned, errors


def validate_email_like(value, label):
    value = clean_text(value)
    if not value:
        return None
    if '@' not in value or '.' not in value.split('@')[-1]:
        return f"{label} must be a valid email address."
    return None


def parse_optional_float(value, label, min_value=None, max_value=None):
    value = clean_text(value)
    if not value:
        return None, None

    try:
        parsed = float(value)
    except ValueError:
        return None, f"{label} must be a number."

    if min_value is not None and parsed < min_value:
        return None, f"{label} must be at least {min_value}."
    if max_value is not None and parsed > max_value:
        return None, f"{label} must be at most {max_value}."

    return parsed, None


def parse_temperature(value, label='Temperature'):
    return parse_optional_float(value, label, min_value=-30, max_value=60)


def parse_humidity(value, label='Humidity'):
    return parse_optional_float(value, label, min_value=0, max_value=100)


def validate_optional_date(value, label):
    value = clean_text(value)
    if not value:
        return None

    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        return f"{label} must use YYYY-MM-DD format."
    return None
