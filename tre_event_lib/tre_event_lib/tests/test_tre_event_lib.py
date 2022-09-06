"""
Tests for tre_event_api module.
"""
import unittest
import time
import jsonschema
import test_utils
from tre_event_lib import tre_event_api

EVENT_BAGIT_AVAILABLE = 'bagit-available'
ENVIRONMENT = 'unittest'
TRE_EVENT = 'tre-event'
TRE_EVENT_ID_KEY = '$id'
TRE_EVENT_ID = 'https://nationalarchives.gov.uk/da-transform/tre/schemas/tre-event'

# Load example event and extract parameters section for test
event_bagit_available = test_utils.load_test_event(
    event_file_name='bagit-available.json'
)

event_bagit_available_parameters = event_bagit_available['parameters']


class TestEventLibCreateEvent(unittest.TestCase):
    """Tests for create_event method."""
    def test_create_event_with_no_prior_event(self):
        """Test basic new event creation works"""
        start_ns = time.time_ns()

        event_1 = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='alpha',
            process='bravo',
            event_name=EVENT_BAGIT_AVAILABLE,
            parameters=event_bagit_available_parameters
        )

        self.assertTrue(isinstance(event_1, dict))
        self.assertTrue('version' in event_1)
        self.assertTrue('timestamp' in event_1)
        self.assertTrue(isinstance(event_1['timestamp'], int))
        self.assertTrue(
            int(event_1['timestamp']) >= start_ns,
            f'{event_1["timestamp"]} / {start_ns}'
        )
        self.assertTrue('UUIDs' in event_1)
        self.assertTrue(len(event_1['UUIDs']) == 1)
        self.assertTrue('producer' in event_1)
        self.assertTrue('parameters' in event_1)

    def test_event_chaining(self):
        """Test event chaining works."""
        CONSIGNMENT_TYPE = 'judgment'
        event_1 = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='alpha',
            process='foo',
            consignment_type=CONSIGNMENT_TYPE,
            event_name=EVENT_BAGIT_AVAILABLE,
            parameters=event_bagit_available_parameters
        )

        event_2 = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='bravo',
            process='bar',
            event_name=EVENT_BAGIT_AVAILABLE,
            parameters=event_bagit_available_parameters,
            prior_event=event_1
        )

        event_3 = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='charlie',
            process='baz',
            event_name=EVENT_BAGIT_AVAILABLE,
            parameters=event_bagit_available_parameters,
            prior_event=event_2
        )

        key_uuids = tre_event_api.KEY_UUIDS
        self.assertTrue(isinstance(event_3[key_uuids], list))
        self.assertTrue(len(event_1[key_uuids]) == 1)
        self.assertTrue(len(event_2[key_uuids]) == 2)
        self.assertTrue(len(event_3[key_uuids]) == 3)
        self.assertTrue('alpha-UUID' == list(event_3[key_uuids][0])[0])
        self.assertTrue('bravo-UUID' == list(event_3[key_uuids][1])[0])
        self.assertTrue('charlie-UUID' == list(event_3[key_uuids][2])[0])
        self.assertTrue('alpha' == event_1['producer']['name'])
        self.assertTrue('bravo' == event_2['producer']['name'])
        self.assertTrue('charlie' == event_3['producer']['name'])
        self.assertTrue('foo' == event_1['producer']['process'])
        self.assertTrue('bar' == event_2['producer']['process'])
        self.assertTrue('baz' == event_3['producer']['process'])
        self.assertTrue(CONSIGNMENT_TYPE == event_1['producer']['type'])
        self.assertTrue(CONSIGNMENT_TYPE == event_2['producer']['type'])
        self.assertTrue(CONSIGNMENT_TYPE == event_3['producer']['type'])

    def test_create_event_fails_with_invalid_event_name(self):
        """Confirm an invalid event-name fails (it will have no schema)."""
        try:
            tre_event_api.create_event(
                environment=ENVIRONMENT,
                producer='alpha',
                process='bravo',
                event_name='no-such-event-as-this-exists',
                parameters=event_bagit_available_parameters
            )

            self.fail('Did not get expected exception')
        except FileNotFoundError as fnf_error:
            self.assertTrue('No such file or directory' in str(fnf_error))
            self.assertTrue('no-such-event-as-this-exists.json' in str(fnf_error))

class TestEventLibValidateEvent(unittest.TestCase):
    """Tests for validate_event method."""
    def test_validate_event_fails_with_missing_uuids(self):
        """Ensure schema validation fails when no UUIDs present."""
        try:
            event_1 = tre_event_api.create_event(
                environment=ENVIRONMENT,
                producer='alpha',
                process='bravo',
                event_name=EVENT_BAGIT_AVAILABLE,
                parameters=event_bagit_available_parameters
            )

            del event_1['UUIDs']
            tre_event_api.validate_event(event=event_1)

            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as v_error:
            self.assertTrue("'UUIDs' is a required property" in str(v_error))


class TestEventLibHelperMethods(unittest.TestCase):
    """Check helper methods work as expected."""
    def test_schema_list(self):
        """Confirm we get a list of schemas."""
        schema_list = tre_event_api.get_event_list()
        self.assertTrue(isinstance(schema_list, list))
        self.assertTrue(TRE_EVENT in schema_list)
        self.assertTrue(EVENT_BAGIT_AVAILABLE in schema_list)

    def test_get_schema(self):
        """Confirm get_event_schema works."""
        schema = tre_event_api.get_event_schema(event_name=TRE_EVENT)
        self.assertEqual(schema[TRE_EVENT_ID_KEY], TRE_EVENT_ID)

    def test_get_schema_store(self):
        """Confirm get_schema_store works."""
        schema_store = tre_event_api.get_schema_store()
        self.assertTrue(isinstance(schema_store, dict))
        self.assertTrue(TRE_EVENT_ID in schema_store)
        self.assertTrue(TRE_EVENT_ID_KEY in schema_store[TRE_EVENT_ID])
