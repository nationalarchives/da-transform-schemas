"""
Tests for bagit-validation-error event.
"""
import unittest
import tre_event_lib
import test_utils
import jsonschema


event_valid = test_utils.load_test_event(
    event_file_name='bagit-validation-error.json')

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='bagit-validation-error-invalid-event-name.json')

EVENT_NAME = 'bagit-validation-error'


class TestBagItValidationErrorSchema(unittest.TestCase):
    def test_event_valid(self):
        tre_event_lib.validate_event(event=event_valid)

    def test_invalid_parameter_event_name(self):
        try:
            tre_event_lib.validate_event(
                event=event_invalid_event_name,
                event_name=EVENT_NAME)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            expected = "'bar' is not one of ['bagit-validation-error']"
            self.assertTrue(expected in str(e))
