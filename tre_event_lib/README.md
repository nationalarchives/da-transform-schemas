To run unit tests:

```bash
python3 -m unittest discover ./tre_event_lib/tests -p 'test_*.py'
```

Note:

The `tre_schemas` directory is currently linked into the `tre_event_lib`
directory with the following:

```bash
# From project root:
ln -s ../tre_schemas tre_event_lib/tre_schemas
```
