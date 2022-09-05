"""
Tests for dri-preingest-sip-accessible event.
"""
import unittest
import tre_event_lib
import test_utils
import jsonschema


event_valid = test_utils.load_test_event(
    event_file_name='dri-preingest-sip-accessible.json'
)

event_invalid_event_name = test_utils.load_test_event(
    event_file_name='dri-preingest-sip-accessible-error.json'
)

EVENT_NAME = 'dri-preingest-sip-accessible'


class TestDirPreingestSipAccessibleSchema(unittest.TestCase):
    def test_event_valid(self):
        tre_event_lib.validate_event(event=event_valid)

    def test_event_invalid_event_name(self):
        try:
            tre_event_lib.validate_event(
                event=event_invalid_event_name,
                event_name=EVENT_NAME)
            
            self.fail('Did not get expected exception')
        except jsonschema.exceptions.ValidationError as e:
            expected = "'oops' is not one of ['preingest_sip_accessible']"
            self.assertTrue(expected in str(e))
