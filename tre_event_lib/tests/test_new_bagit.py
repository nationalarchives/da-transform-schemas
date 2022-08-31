"""
Tests for new-bagit event.
"""
import logging
import os
import unittest
import tre_event_lib
import json

logger = logging.getLogger(__name__)


def setup_logging(
    default_config_file='logging.json',
    default_level=logging.INFO,
    log_config_env_key='LOG_CONFIG_JSON'
):
    """
    Setup module logging.
    """
    env_key_path = os.getenv(log_config_env_key, None)
    config_file = env_key_path if env_key_path else default_config_file
    if os.path.exists(config_file):
        with open(config_file, 'rt', encoding='utf-8') as f:
            logging.config.dictConfig(json.load(f.read()))
    else:
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=default_level, format=format_str)


EVENT_NEW_BAGIT = 'new-bagit'
ENVIRONMENT = 'unittest'


event_valid_new_bagit_1 = {
    'version': '1.0.0',
    'timestamp': 42,
    'UUIDs': [
        {'foo-UUID': '8d02ec4d-550c-4af7-849b-c5cef5f8e820'}
    ],
    'producer': {
        'name': 'foo',
        'environment': 'foo',
        'process': 'foo',
        'event-name': EVENT_NEW_BAGIT,
        'type': None
    },
    'parameters': {
        EVENT_NEW_BAGIT: {
            'resource': {
                'resource-type': '',
                'access-type': '',
                'value': ''
            },
            'resource-validation': {
                'resource-type': '',
                'access-type': '',
                'validation-method': '',
                'value': '',
            },
            'reference' : ''
        }
    }
}


class TestEventLibValidateNewBagitEvent(unittest.TestCase):
    def test_validate_event(self):
        tre_event_lib.validate_event(event=event_valid_new_bagit_1)


setup_logging(default_level=logging.WARN)
