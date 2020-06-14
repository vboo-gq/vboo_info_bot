"""Test configuration"""

import os

from rival_regions_wrapper import LocalAuthentication, ApiWrapper
from dotenv import load_dotenv
import pytest


load_dotenv()

class MissingAuthenticationError(Exception):
    """Error for missing authentication"""


@pytest.fixture(scope="module")
def api_wrapper():
    """Set up wrapper before test"""
    rr_username = os.environ.get('RIVAL_REGIONS_USERNAME', None)
    rr_password = os.environ.get('RIVAL_REGIONS_PASSWORD', None)
    rr_login_method = os.environ.get('RIVAL_REGIONS_LOGIN_METHOD', None)
    if None in (rr_username, rr_password, rr_login_method):
        raise MissingAuthenticationError(
            'Load the following variables in your user environment: '
            'RIVAL_REGIONS_USERNAME, RIVAL_REGIONS_PASSWORD, RIVAL_REGIONS_LOGIN_METHOD'
        )
    authentication = LocalAuthentication(rr_username, rr_password, rr_login_method)
    return ApiWrapper(authentication)