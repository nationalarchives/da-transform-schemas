"""
Helper code for event testing.
"""
import os
import sys
import json

def load_test_event(event_file_name: str) -> dict:
    test_event_dir = 'test_events'
    file_path = os.path.join(sys.path[0], test_event_dir, event_file_name)
    with open(file_path, 'rt', encoding='utf-8') as fp:
        return json.load(fp=fp)
