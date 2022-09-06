"""
Tests for bagit-validated event.
"""
import unittest
import test_utils
import jsonschema
from tre_event_lib import tre_event_api


event_valid = test_utils.load_test_event(
    event_file_name='dri-preingest-sip-available.json')

event_invalid_parameter_name = test_utils.load_test_event(
    event_file_name='dri-preingest-sip-available-error.json')

EVENT_NAME = 'dri-preingest-sip-available'


class TestDriPreingestSipAvailableSchema(unittest.TestCase):
    """Tests for dri-preingest-sip-available event."""
    def test_event_valid(self):
        """Test dri-preingest-sip-available schema."""
        tre_event_api.validate_event(event=event_valid)

    def test_invalid_parameter_name(self):
        """Test dri-preingest-sip-available schema fails with invalid event-name."""

        try:
            tre_event_api.validate_event(
                event=event_invalid_parameter_name,
                schema_name=EVENT_NAME)

            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as validation_error:
            expected = "34234132423 is not of type 'string'"
            self.assertTrue(expected in str(validation_error))

