"""
Tests for judgment-parser-error event.
"""
import unittest
import test_utils
import jsonschema
from tre_event_lib import tre_event_api


event_valid = test_utils.load_test_event(
    event_file_name='judgment-parser-error.json'
)

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='judgment-parser-error-invalid-event-name.json')

EVENT_NAME = 'judgment-parser-error'


class TestJudgmentAvailable(unittest.TestCase):
    """Tests for judgment-parser-error event."""
    def test_event_valid(self):
        """Test judgment-parser-error schema."""
        tre_event_api.validate_event(event=event_valid)

    def test_event_invalid_event_name(self):
        """Test judgment-parser-error schema fails when event-name invalid."""
        try:
            tre_event_api.validate_event(
                event=event_invalid_event_name,
                schema_name=EVENT_NAME)  # intended schema (as name invalid)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as validation_error:
            expected = "'invalid-event-name-jpe' is not one of ['judgment-parser-error']"
            self.assertTrue(expected in str(validation_error))
