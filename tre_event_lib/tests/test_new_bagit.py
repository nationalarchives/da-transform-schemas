"""
Tests for new-bagit event.
"""
import unittest
import tre_event_api
import test_utils
import jsonschema


event_valid = test_utils.load_test_event(
    event_file_name='new-bagit.json'
)

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='new-bagit-invalid-event-name.json'
)

EVENT_NAME = 'new-bagit'


class TestNewBagitSchema(unittest.TestCase):
    def test_event_valid(self):
        tre_event_api.validate_event(event=event_valid)

    def test_event_invalid_event_name(self):
        try:
            tre_event_api.validate_event(
                event=event_invalid_event_name,
                event_name=EVENT_NAME)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            expected = "'oops' is not one of ['new-bagit']"
            self.assertTrue(expected in str(e))
