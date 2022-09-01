"""
Tests for tre_event_lib module.
"""
import logging
import os
import unittest
import tre_event_lib
import json
import time
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


EVENT_NEW_BAGIT = 'new-bagit'
ENVIRONMENT = 'unittest'
TRE_EVENT = 'tre-event'
TRE_EVENT_ID_KEY = '$id'
TRE_EVENT_ID = 'https://nationalarchives.gov.uk/da-transform/tre/schemas/tre-event'

event_new_bagit_parameters = {
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


class TestEventLibCreateEvent(unittest.TestCase):
    def test_create_event_with_no_prior_event(self):
        start_ns = time.time_ns()

        e = tre_event_lib.create_event(
            environment=ENVIRONMENT,
            producer='alpha',
            process='bravo',
            event_name=EVENT_NEW_BAGIT,
            parameters=event_new_bagit_parameters
        )

        logger.info(f'test_create_event_with_no_prior_event e={e}')

        self.assertTrue(isinstance(e, dict))
        self.assertTrue('version' in e)
        self.assertTrue('timestamp' in e)
        self.assertTrue(isinstance(e['timestamp'], int))
        self.assertTrue(
            int(e['timestamp']) >= start_ns, f'{e["timestamp"]} / {start_ns}')
        self.assertTrue('UUIDs' in e)
        self.assertTrue(len(e['UUIDs']) == 1)
        self.assertTrue('producer' in e)
        self.assertTrue('parameters' in e)
        

    def test_create_event_fails_with_invalid_event_name(self):
        try:
            tre_event_lib.create_event(
                environment=ENVIRONMENT,
                producer='alpha',
                process='bravo',
                event_name='no-such-event-as-this-exists',
                parameters=event_new_bagit_parameters
            )

            self.fail('Did not get expected exception')
        except FileNotFoundError as e:
            self.assertTrue('No such file or directory' in str(e))
            self.assertTrue('no-such-event-as-this-exists.json' in str(e))


    def test_create_event_fails_with_missing_uuids(self):
        try:
            e = tre_event_lib.create_event(
                environment=ENVIRONMENT,
                producer='alpha',
                process='bravo',
                event_name=EVENT_NEW_BAGIT,
                parameters=event_new_bagit_parameters
            )

            del e['UUIDs']
            tre_event_lib.validate_event(event=e)

            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            self.assertTrue("'UUIDs' is a required property" in str(e))


class TestEventLibHelperMethods(unittest.TestCase):
    def test_schema_list(self):
        schema_list = tre_event_lib.get_event_list()
        self.assertTrue(isinstance(schema_list, list))
        self.assertTrue(TRE_EVENT in schema_list)
        self.assertTrue(EVENT_NEW_BAGIT in schema_list)

    def test_get_schema(self):
        schema = tre_event_lib.get_event_schema(event_name=TRE_EVENT)
        self.assertEqual(schema[TRE_EVENT_ID_KEY], TRE_EVENT_ID)

    def test_get_schema_store(self):
        ssd = tre_event_lib.get_schema_store()
        self.assertTrue(isinstance(ssd, dict))
        self.assertTrue(TRE_EVENT_ID in ssd)
        self.assertTrue(TRE_EVENT_ID_KEY in ssd[TRE_EVENT_ID])


setup_logging(default_level=logging.WARN)
