"""
Tests for new-bagit event.
"""
import logging
import os
import unittest
import tre_event_lib
import json
import test_utils
import jsonschema

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


event_valid = test_utils.load_test_event(
    event_file_name='new-bagit.json'
)

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='new-bagit-invalid-event-name.json'
)

EVENT_NAME = 'new-bagit'


class TestNewBagitSchema(unittest.TestCase):
    def test_event_valid(self):
        tre_event_lib.validate_event(event=event_valid)

    def test_event_invalid_event_name(self):
        try:
            tre_event_lib.validate_event(
                event=event_invalid_event_name,
                event_name=EVENT_NAME)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            expected = "'oops' is not one of ['new-bagit']"
            self.assertTrue(expected in str(e))


setup_logging(default_level=logging.WARN)
