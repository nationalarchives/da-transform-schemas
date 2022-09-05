# About

A Python package that contains:

* JSON schemas for TRE events
* A Python API to:
  * Create (optionally chained) TRE events
  * Validate TRE events against their respective JSON schemas

# Example Use

```python
from tre_event_lib import tre_event_api

# To validate event using schema derived from event's provider.event-name field:
tre_event_api.validate_event(event=some_event)

# To validate event against a specific schema (e.g. root tre-event.json schema)
tre_event_api.validate_event(event=some_event, schema_name='tre-event')

# Creating (and therefore validating) an event from a prior (incoming) event
new_event_params = { 'bagit-validated': { ... }}
bagit_valdiated_event = tre_event_api.create_event(
    environment=ENVIRONMENT,
    producer='bravo',
    process='bar',
    event_name='bagit-validated',
    parameters=new_event_params,
    prior_event=prior_event_dict  # e.g. sourced from Lambda handler input
)

# To list available event names that have a corresponding schema
tre_event_api.get_event_list()

# To view a JSON schema
tre_event_api.get_event_schema(event_name='tre-event')
```

# Development

## Running Unit Tests

```bash
# Ensure jsonschema package is installed in the current environment
pip3 install jsonschema
```

```bash
cd tre_event_lib

# All tests:
python3 -m unittest discover ./tre_event_lib/tests -p 'test_*.py'

# An individual test:
python3 -m unittest discover ./tre_event_lib/tests -p 'test_bagit_received.py'
```

To build Python `whl` package with API and schemas:

```bash
cd tre_event_lib
./build.sh
```

## Testing In Docker

```bash
# Run this from project root to map /host to all the repo's files
docker run \
  --tty \
  --interactive \
  --rm \
  --mount "type=bind,source=${PWD},target=/host,readonly" \
  --entrypoint bash \
  python:3.8.13-buster

# 3.9
docker run \
  --tty \
  --interactive \
  --rm \
  --mount "type=bind,source=${PWD},target=/host,readonly" \
  --entrypoint bash \
  python:3.9.13-bullseye
```

```bash
# To install libraries from container's CLI:
pip3 install jsonschema \
&& pip3 install "$(find /host/tre_event_lib/dist -name '*.whl')"
```

```bash
# Python examples
python3 -c 'from tre_event_lib import tre_event_api; print(tre_event_api.EVENT_VERSION)'
python3 -c 'from tre_event_lib import tre_event_api; print(tre_event_api.get_event_list())'
python3 -c 'from tre_event_lib import tre_event_api; print(tre_event_api.get_schema_store())'

# Or just run a Python shell...
python3
```
