"""
Module to support TRE event handling with JSON schema validation.
"""
import logging
import logging.config
import os
import pkgutil
import json
import time
import uuid
import jsonschema
import pkg_resources

logger = logging.getLogger(__name__)

def setup_logging(
    default_config_file='logging.json',
    default_level=logging.INFO,
    log_config_env_key='LOG_CONFIG_JSON'
):
    """
    Setup module logging.
    """
    env_key_path = os.getenv(log_config_env_key, None)
    config_file = env_key_path if env_key_path else default_config_file
    if os.path.exists(config_file):
        with open(config_file, 'rt', encoding='utf-8') as file_ptr:
            logging.config.dictConfig(json.load(file_ptr))
    else:
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=default_level, format=format_str)

setup_logging(default_level=logging.INFO)

KEY_VERSION = 'version'
KEY_TIMESTAMP = 'timestamp'
KEY_UUIDS = 'UUIDs'
UUID_KEY_SUFFIX = '-UUID'
KEY_PRODUCER = 'producer'
KEY_NAME = 'name'
KEY_PROCESS = 'process'
KEY_TYPE = 'type'
KEY_EVENT_NAME = 'event-name'
KEY_ENVIRONMENT = 'environment'
KEY_PARAMETERS = 'parameters'
KEY_REFERENCE = 'reference'
KEY_S3_BUCKET = 's3-bucket'
KEY_ERRORS = 'errors'

ROOT_EVENT = 'tre-event'
SCHEMA_SUFFIX = '.json'
KEY_SCHEMA_ID = '$id'
MANIFEST = 'manifest.json'
ABOUT = 'about.json'
KEY_ABOUT_VERSION = 'version'
PACKAGE_NAME='tre_event_lib'
MODULE_NAME='tre_event_api'
SCHEMA_DIR = 'tre_schemas'

# Get version info from about.json (created at build time with git tag version)
about = {
    KEY_ABOUT_VERSION: None
}

if __name__ =='__main__':
    # Handle case of running locally, not as whl import
    about_file = os.path.join(os.path.dirname(__file__), ABOUT)
    with open(about_file, 'rt', encoding='utf-8') as fp:
        about = json.load(fp=fp)
else:
    about = json.loads(
        pkgutil.get_data(
            package=__name__,
            resource=ABOUT
        ).decode()
    )

EVENT_VERSION = about[KEY_ABOUT_VERSION]


def get_event_list() -> list:
    """
    Lists available event names from package's tre_schemas dir.
    """
    event_list = []

    # Consider migrating to importlib.resources.files
    for name in pkg_resources.resource_listdir(PACKAGE_NAME, SCHEMA_DIR):
        event_list.append(name[:-5])  # strip '.json'

    return event_list


def get_event_schema(event_name: str = ROOT_EVENT) -> str:
    """
    Returns the JSON schema for a given event name.
    """
    schema_resource = os.path.join(SCHEMA_DIR, event_name + SCHEMA_SUFFIX)
    logger.info('Loading schema "%s" for event "%s"', schema_resource, event_name)
    schema = json.loads(
        pkgutil.get_data(
            package=__name__,
            resource=schema_resource
        ).decode()
    )

    logger.info('Validating schema "%s"', schema_resource)
    jsonschema.Validator.check_schema(schema=schema)
    logger.info('Schema "%s" validated', schema_resource)
    return schema


def get_schema_store() -> dict:
    """
    Returns a dictionary of schemas as required by the jsonschema library.
    """
    schema_store_dict = {}
    event_list = get_event_list()
    logger.info('event_list={%s}', event_list)

    for event in event_list:
        schema = get_event_schema(event_name=event)
        if KEY_SCHEMA_ID not in schema:
            raise ValueError(f'Key "{KEY_SCHEMA_ID}" not found in schema for '
                f'event "{event}"')
        schema_store_dict[schema[KEY_SCHEMA_ID]] = schema

    return schema_store_dict


def validate_event(
    event: dict,
    schema_name: str = None
):
    """
    Validate `event` against the JSON schema that matches the event name in
    field `event.producer.event-name`, unless a specific `schema_name` is
    passed, in which case validate with that JSON schema instead.
    """
    logger.info('Validating event=%s schema_name=%s', event, schema_name)

    # If no event name specified, use event's event-name field
    if not schema_name:
        schema_name = event[KEY_PRODUCER][KEY_EVENT_NAME]

    logger.info('schema_name=%s', schema_name)
    schema = get_event_schema(event_name=schema_name)
    logger.info('schema=%s', schema)

    resolver = jsonschema.RefResolver.from_schema(
        schema=schema,
        store=get_schema_store()
    )

    jsonschema.Draft202012Validator(
        schema=schema,
        resolver=resolver
    ).validate(event)


def create_event(
    environment: str,
    producer: str,
    process: str,
    event_name: str,
    parameters: dict,
    consignment_type: str = None,  # consignment_type as "type" shadows Python
    prior_event: dict = None,
    event_schema_name: str = None,
    prior_event_schema_name: str = None
) -> dict:
    """
    Create a TRE event from the given arguments. The event has a new UUID
    appended to its UUID list and it is assigned a current timestamp value.

    If `prior_event` is given:
    * It is validated against its schema (which is determined by its
      `producer.event-name` field, unless prior_event_schema_name given)
    * The prior message's UUID list is prepended to the new event's UUID list
    * If the `consignment_type` argument is not given, the prior message's
      consignment type is used for the new event

    The final event is validated against its schema (which is determined by its
    `producer.event-name` field, unless prior_event_schema_name given)
    """
    timestamp_ns_utc = time.time_ns()

    event_uuids = []
    if prior_event:
        logger.info('prior_event found')
        validate_event(event=prior_event, schema_name=prior_event_schema_name)
        logger.info('copying prior_event UUIDs')
        # Use [:] to copy (not reference) prior UUIDs
        event_uuids = prior_event[KEY_UUIDS][:]        
    else:
        logger.info('no prior_event found')

    # Create new UUID and corresponding key name (with producer name)
    key_uuid = f'{producer}{UUID_KEY_SUFFIX}'
    event_uuid = str(uuid.uuid4())
    logger.info('key_uuid=%s event_uuid=%s', key_uuid, event_uuid)
    event_uuids.append({key_uuid: event_uuid})

    # Set event's type; prefer consignment_type parameter, fall back to prior
    # message type
    event_type = None
    if consignment_type:
        logger.info('event_type set explicitly')
        event_type = consignment_type
    elif (
        prior_event
        and (KEY_PRODUCER in prior_event)
        and (KEY_TYPE in prior_event[KEY_PRODUCER])
    ):
        logger.info('event_type set from prior_event')
        event_type = prior_event[KEY_PRODUCER][KEY_TYPE]
    else:
        logger.info('event_type not set')

    event_producer = {
        KEY_ENVIRONMENT: environment,
        KEY_NAME: producer,
        KEY_PROCESS: process,
        KEY_EVENT_NAME: event_name,
        KEY_TYPE: event_type
    }

    event = {
        KEY_VERSION: EVENT_VERSION,
        KEY_TIMESTAMP: timestamp_ns_utc,
        KEY_UUIDS: event_uuids,
        KEY_PRODUCER: event_producer,
        KEY_PARAMETERS: parameters
    }

    validate_event(event=event, schema_name=event_schema_name)
    return event
