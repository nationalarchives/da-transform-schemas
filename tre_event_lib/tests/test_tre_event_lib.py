"""
Tests for tre_event_api module.
"""
import unittest
import tre_event_api
import time
import jsonschema
import test_utils

EVENT_NEW_BAGIT = 'new-bagit'
ENVIRONMENT = 'unittest'
TRE_EVENT = 'tre-event'
TRE_EVENT_ID_KEY = '$id'
TRE_EVENT_ID = 'https://nationalarchives.gov.uk/da-transform/tre/schemas/tre-event'

# Load example event and extract parameters section for test
event_new_bagit = test_utils.load_test_event(
    event_file_name='new-bagit.json'
)

event_new_bagit_parameters = event_new_bagit['parameters']


class TestEventLibCreateEvent(unittest.TestCase):
    def test_create_event_with_no_prior_event(self):
        start_ns = time.time_ns()

        e = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='alpha',
            process='bravo',
            event_name=EVENT_NEW_BAGIT,
            parameters=event_new_bagit_parameters
        )

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


    def test_event_chaining(self):
        e1 = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='alpha',
            process='foo',
            event_name=EVENT_NEW_BAGIT,
            parameters=event_new_bagit_parameters
        )

        e2 = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='bravo',
            process='bar',
            event_name=EVENT_NEW_BAGIT,
            parameters=event_new_bagit_parameters,
            prior_message=e1
        )

        e3 = tre_event_api.create_event(
            environment=ENVIRONMENT,
            producer='charlie',
            process='baz',
            event_name=EVENT_NEW_BAGIT,
            parameters=event_new_bagit_parameters,
            prior_message=e2
        )

        print(e1)
        print(e2)
        print(e3)
        key_uuids = tre_event_api.KEY_UUIDS
        self.assertTrue(isinstance(e3[key_uuids], list))
        self.assertTrue(len(e1[key_uuids]) == 1)
        self.assertTrue(len(e2[key_uuids]) == 2)
        self.assertTrue(len(e3[key_uuids]) == 3)
        self.assertTrue('alpha-UUID' == list(e3[key_uuids][0])[0])
        self.assertTrue('bravo-UUID' == list(e3[key_uuids][1])[0])
        self.assertTrue('charlie-UUID' == list(e3[key_uuids][2])[0])
        self.assertTrue('alpha' == e1['producer']['name'])
        self.assertTrue('bravo' == e2['producer']['name'])
        self.assertTrue('charlie' == e3['producer']['name'])
        self.assertTrue('foo' == e1['producer']['process'])
        self.assertTrue('bar' == e2['producer']['process'])
        self.assertTrue('baz' == e3['producer']['process'])


    def test_create_event_fails_with_invalid_event_name(self):
        try:
            tre_event_api.create_event(
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
            e = tre_event_api.create_event(
                environment=ENVIRONMENT,
                producer='alpha',
                process='bravo',
                event_name=EVENT_NEW_BAGIT,
                parameters=event_new_bagit_parameters
            )

            del e['UUIDs']
            tre_event_api.validate_event(event=e)

            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            self.assertTrue("'UUIDs' is a required property" in str(e))


class TestEventLibHelperMethods(unittest.TestCase):
    def test_schema_list(self):
        schema_list = tre_event_api.get_event_list()
        self.assertTrue(isinstance(schema_list, list))
        self.assertTrue(TRE_EVENT in schema_list)
        self.assertTrue(EVENT_NEW_BAGIT in schema_list)

    def test_get_schema(self):
        schema = tre_event_api.get_event_schema(event_name=TRE_EVENT)
        self.assertEqual(schema[TRE_EVENT_ID_KEY], TRE_EVENT_ID)

    def test_get_schema_store(self):
        ssd = tre_event_api.get_schema_store()
        self.assertTrue(isinstance(ssd, dict))
        self.assertTrue(TRE_EVENT_ID in ssd)
        self.assertTrue(TRE_EVENT_ID_KEY in ssd[TRE_EVENT_ID])
