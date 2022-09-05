To run unit tests:

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

Docker Testing Notes:

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
