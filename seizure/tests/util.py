import os
from unittest import skip
from unittest.case import _id


def skip_if_local(reason):
    """
    Skip a test if environment variable 'LOCAL' is True
    """
    if bool_env('LOCAL'):
        return skip(reason)
    return _id


def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if os.environ.get(val, False) == 'True' else False
