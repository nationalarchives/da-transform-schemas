# About

A Python package that contains:

* TRE event [JSON schemas](../tre_schemas/)
* A [Python API](tre_event_lib/tre_event_api.py) to:
  * Create (optionally chained) TRE event payloads
  * Validate TRE events against their respective JSON schemas

# Example Use

> To build the project's `whl` file, see the [Package Build Process](#package-build-process)
  section

```bash
pip3 install jsonschema
pip3 install "$(find /host/tre_event_lib/dist -name '*.whl')"
python3
```

```python
from tre_event_lib import tre_event_api

# To validate event using schema derived from event's provider.event-name field:
tre_event_api.validate_event(
    event=some_event_dict  # e.g. sourced from Lambda handler input
)

# To validate event against a specific schema (e.g. root tre-event.json schema)
tre_event_api.validate_event(
    event=some_event_dict,  # e.g. sourced from Lambda handler input
    schema_name='tre-event'
)

# Creating (and therefore validating) an event from a prior (incoming) event
new_event_params = {
    'bagit-validated': {}  # example event parameter value; not complete
}

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

## Package Build Process

To build Python `whl` package with API and schemas:

```bash
pip3 install jsonschema
cd tre_event_lib

# Pass a version to not use latest git tag version
./build.sh ${version_if_not_latest_git_tag}
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
