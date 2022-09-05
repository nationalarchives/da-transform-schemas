"""
Tests for bagit-received event.
"""
import unittest
import jsonschema
import test_utils
from tre_event_lib import tre_event_api


event_valid = test_utils.load_test_event(
    event_file_name='bagit-received.json')

event_invalid_params = test_utils.load_test_event(
    event_file_name='bagit-received-invalid-params.json')

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='bagit-received-invalid-event-name.json')

EVENT_NAME = 'bagit-received'


class TestBagItReceivedSchema(unittest.TestCase):
    """Test bagit_received schema"""
    def test_event_valid(self):
        """Test valid event scenario"""
        tre_event_api.validate_event(event=event_valid)

    def test_event_invalid_parameters(self):
        """Verify invalid parameter values fail"""
        try:
            tre_event_api.validate_event(event=event_invalid_params)
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as v_err:
            expected = (
                "Failed validating 'required' in schema['properties']"
                "['parameters']['properties']['bagit-received']"
            )
            self.assertTrue(expected in str(v_err))

    def test_invalid_parameter_event_name(self):
        """Verify invalid event-name fails"""
        try:
            tre_event_api.validate_event(
                event=event_invalid_event_name,
                schema_name=EVENT_NAME)  # specify as test event name is invalid

            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as v_err:
            expected = "'nosuch' is not one of ['bagit-received']"
            self.assertTrue(expected in str(v_err))
