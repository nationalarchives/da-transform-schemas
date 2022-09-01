To run unit tests:

```bash
cd tre_event_lib
python3 -m unittest discover ./tests -p 'test_*.py'
```

Note:

The `tre_schemas` directory is currently linked into the `tre_event_lib`
directory with the following:

```bash
# From project root:
ln -s ../tre_schemas tre_event_lib/tre_schemas
```

Docker Testing Notes:

```bash
# Run from project root to map /host to repo's files
docker run \
  --tty \
  --interactive \
  --rm \
  --mount "type=bind,source=${PWD},target=/host,readonly" \
  --entrypoint bash \
  python:3.8.13-buster
```

```bash
# Install libraries
pip3 install "$(find /host/tre_event_lib/dist -name '*.whl')" \
  && pip3 install jsonschema
```

```bash
# Python examples
python3 -c 'import tre_event_lib; print(tre_event_lib.EVENT_VERSION)'
python3 -c 'import tre_event_lib; print(tre_event_lib.get_schema_store())'

# Or run Python shell
python3
```
