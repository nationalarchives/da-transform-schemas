"""
Tests for bagit-received event.
"""
import unittest
import tre_event_lib
import test_utils
import jsonschema


event_valid = test_utils.load_test_event(
    event_file_name='bagit-received.json')

event_invalid_params = test_utils.load_test_event(
    event_file_name='bagit-received-invalid-params.json')

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='bagit-received-invalid-event-name.json')

EVENT_NAME = 'bagit-received'


class TestBagItReceivedSchema(unittest.TestCase):
    def test_event_valid(self):
        tre_event_lib.validate_event(event=event_valid)

    def test_event_invalid_parameters(self):
        try:
            tre_event_lib.validate_event(event=event_invalid_params)
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            expected = "Failed validating 'required' in schema['properties']['parameters']['properties']['bagit-received']"
            self.assertTrue(expected in str(e))

    def test_invalid_parameter_event_name(self):
        try:
            tre_event_lib.validate_event(
                event=event_invalid_event_name,
                event_name=EVENT_NAME)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            expected = "'new-bagit' is not one of ['bagit-received']"
            self.assertTrue(expected in str(e))
