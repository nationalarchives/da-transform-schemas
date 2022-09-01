"""
Tests for bagit-validated event.
"""
import unittest
import tre_event_lib
import test_utils
import jsonschema


event_valid = test_utils.load_test_event(
    event_file_name='bagit-validated.json')

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='bagit-validated-invalid-event-name.json')

EVENT_NAME = 'bagit-validated'


class TestBagItValidatedSchema(unittest.TestCase):
    def test_event_valid(self):
        tre_event_lib.validate_event(event=event_valid)

    def test_invalid_parameter_event_name(self):
        try:
            tre_event_lib.validate_event(
                event=event_invalid_event_name,
                event_name=EVENT_NAME)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            expected = "'delta' is not one of ['bagit-validated']"
            self.assertTrue(expected in str(e))
