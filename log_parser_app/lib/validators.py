import re


INT_REGEXP = r'[0-9]+'
STR_1_REGEXP = r'[a-zA-Z0-9_\- ]+'
STR_2_REGEXP = r'[a-zA-Z0-9_\- \[\]]+'


def validate_regexp(
        value, pattern,
        missing_allowed=False, default=None,
        min_len=None, max_len=None
):
    if missing_allowed and not value:
        return default
    if not re.match(pattern, value):
        raise ValueError()
    if any((
        max_len and len(value) > max_len,
        min_len and len(value) < min_len
    )):
        raise ValueError()
    return value


def validate_int(
        value,
        missing_allowed=False, default=None,
        min_len=None, max_len=None,
        min_value=None, max_value=None
):
    int_value = int(validate_regexp(
        value, INT_REGEXP,
        missing_allowed, default,
        min_len, max_len
    ))
    if any((
        max_value and int_value > max_value,
        min_value and int_value < min_value
    )):
        raise ValueError
    return int_value


def validate_str_1(
        value,
        missing_allowed=False, default=None,
        min_len=None, max_len=None
):
    return validate_regexp(
        value, STR_1_REGEXP,
        missing_allowed, default,
        min_len, max_len
    )


def validate_str_2(
        value,
        missing_allowed=False, default=None,
        min_len=None, max_len=None
):
    return validate_regexp(
        value, STR_2_REGEXP,
        missing_allowed, default,
        min_len, max_len
    )


def validate_project_name(
        value,
        missing_allowed=False, default=None,
):
    return validate_str_1(
        value,
        missing_allowed, default,
        min_len=1, max_len=50
    )


def validate_url(
        value,
        missing_allowed=False, default=None,
):
    return value


class Validator(object):

    def __init__(self, value):
        self.value = value


def validate_new_user(**user_data):
    return dict(
        username=user_data.get('username'),
        password=user_data.get('password'),
        email=user_data.get('email'))
