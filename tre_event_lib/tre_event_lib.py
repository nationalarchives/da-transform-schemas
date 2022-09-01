"""
Code to support using TRE event JSON schemas.
"""
import logging
import os
import pkgutil
import json
import time
import uuid
import jsonschema

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
        with open(config_file, 'rt', encoding='utf-8') as f:
            logging.config.dictConfig(json.load(f.read()))
    else:
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=default_level, format=format_str)


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

ROOT_EVENT = 'tre-event'
SCHEMA_PATH = 'tre_schemas/'
SCHEMA_SUFFIX = '.json'
KEY_SCHEMA_ID = '$id'
MANIFEST = 'manifest.json'
ABOUT = 'about.json'


# Get version info from about.json (created at build time with git tag version)
about = json.loads(
    pkgutil.get_data(
        package=__name__,
        resource=ABOUT
    ).decode()
)

EVENT_VERSION = about['version']


def get_event_list() -> list:
    """
    Lists event names in module's manifest file.
    """
    event_list = json.loads(
        pkgutil.get_data(
            package=__name__,
            resource=MANIFEST
        ).decode()
    )

    if not isinstance(event_list, list):
        raise ValueError(f'Event list is type "{type(event_list)}", not list')

    return event_list


def get_event_schema(event_name: str = ROOT_EVENT) -> str:
    """
    Returns the JSON schema for a given event name.
    """
    schema_resource = SCHEMA_PATH + event_name + SCHEMA_SUFFIX
    logger.info(f'Loading schema "{schema_resource}" for event "{event_name}"')
    schema = json.loads(
        pkgutil.get_data(
            package=__name__,
            resource=schema_resource
        ).decode()
    )

    logger.info(f'Validating schema "{schema_resource}"')
    jsonschema.Validator.check_schema(schema=schema)
    logger.info(f'Schema "{schema_resource}" validated')
    return schema


def get_schema_store() -> dict:
    schema_store_dict = {}
    event_list = get_event_list()
    logger.info(f'event_list={event_list}')
    
    for event in event_list:
        schema = get_event_schema(event_name=event)
        if KEY_SCHEMA_ID not in schema:
            raise ValueError(f'Key "{KEY_SCHEMA_ID}" not found in schema for '
                f'event "{event}"')
        schema_store_dict[schema[KEY_SCHEMA_ID]] = schema
    
    return schema_store_dict


def validate_event(
    event: dict
):
    logger.info(f'Validating event={event}')
    event_name = event[KEY_PRODUCER][KEY_EVENT_NAME]
    logger.info(f'event_name={event_name}')
    event_schema = get_event_schema(event_name=event_name)
    logger.info(f'event_schema={event_schema}')

    resolver = jsonschema.RefResolver.from_schema(
        schema=event_schema,
        store=get_schema_store()
    )

    jsonschema.Draft202012Validator(
        schema=event_schema,
        resolver=resolver
    ).validate(event)


def create_event(
    environment: str,
    producer: str,
    process: str,
    event_name: str,
    parameters: dict,
    type: str = None,
    prior_message: dict = None
) -> dict:
    timestamp_ns_utc = time.time_ns()

    event_uuids = []
    if prior_message:
        validate_event(event=prior_message)
        # Use [:] to copy (not reference) prior UUIDs
        event_uuids = prior_message[KEY_UUIDS][:]

    # Create new UUID and corresponding key name (with producer name)
    key_uuid = f'{producer}{UUID_KEY_SUFFIX}'
    event_uuid = str(uuid.uuid4())
    logger.info(f'key_uuid={key_uuid} event_uuid={event_uuid}')
    event_uuids.append({key_uuid: event_uuid})

    # Set event type; prefer type parameter, fall back to prior message type
    event_type = None
    if type:
        event_type = type
    elif prior_message and (KEY_TYPE in prior_message):
        event_type = prior_message[KEY_TYPE]
        
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

    validate_event(event=event)
    return event


if __name__ == "__main__":
    setup_logging(default_level=logging.INFO)
