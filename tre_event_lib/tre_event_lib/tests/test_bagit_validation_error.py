"""
Tests for bagit-validation-error event.
"""
import unittest
import test_utils
import jsonschema
from tre_event_lib import tre_event_api


event_valid = test_utils.load_test_event(
    event_file_name='bagit-validation-error.json')

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='bagit-validation-error-invalid-event-name.json')

EVENT_NAME = 'bagit-validation-error'


class TestBagItValidationErrorSchema(unittest.TestCase):
    """Tests for bagit-validation-error event."""
    def test_event_valid(self):
        """Test bagit-validation-error schema."""
        tre_event_api.validate_event(event=event_valid)

    def test_invalid_parameter_event_name(self):
        """Test bagit-validation-error schema fails with invalid event-name."""
        try:
            tre_event_api.validate_event(
                event=event_invalid_event_name,
                schema_name=EVENT_NAME)  # intended schema (as name invalid)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as validation_error:
            expected = "'bar' is not one of ['bagit-validation-error']"
            self.assertTrue(expected in str(validation_error))
