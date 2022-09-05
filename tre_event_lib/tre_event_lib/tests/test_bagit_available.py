"""
Tests for bagit-available event.
"""
import unittest
import test_utils
import jsonschema
from tre_event_lib import tre_event_api


event_valid = test_utils.load_test_event(
    event_file_name='bagit-available.json'
)

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='bagit-available-invalid-event-name.json'
)

EVENT_NAME = 'bagit-available'


class TestNewBagitSchema(unittest.TestCase):
    """Tests for bagit-available event."""
    def test_event_valid(self):
        """Test bagit-available schema."""
        tre_event_api.validate_event(event=event_valid)

    def test_event_invalid_event_name(self):
        """Test bagit-available schema fails with invalid event-name."""
        try:
            tre_event_api.validate_event(
                event=event_invalid_event_name,
                schema_name=EVENT_NAME)  # intended schema (as name invalid)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as validation_error:
            expected = "'oops' is not one of ['bagit-available']"
            self.assertTrue(expected in str(validation_error))
