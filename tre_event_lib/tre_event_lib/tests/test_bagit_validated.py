"""
Tests for bagit-validated event.
"""
import unittest
import test_utils
import jsonschema
from tre_event_lib import tre_event_api


event_valid = test_utils.load_test_event(
    event_file_name='bagit-validated.json')

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='bagit-validated-invalid-event-name.json')

EVENT_NAME = 'bagit-validated'


class TestBagItValidatedSchema(unittest.TestCase):
    """Tests for bagit-validated event."""
    def test_event_valid(self):
        """Test bagit-validated schema."""
        tre_event_api.validate_event(event=event_valid)

    def test_invalid_parameter_event_name(self):
        """Test bagit-validated schema fails with invalid event-name."""
        try:
            tre_event_api.validate_event(
                event=event_invalid_event_name,
                schema_name=EVENT_NAME)  # intended schema (as name invalid)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as validation_error:
            expected = "'delta' is not one of ['bagit-validated']"
            self.assertTrue(expected in str(validation_error))
