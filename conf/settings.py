import yaml
import os

# read-in default paramerst
with open("./conf/mocker_setup_params.yaml", 'r') as yaml_file:
    MOCKER_SETUP_PARAMS = yaml.safe_load(yaml_file)

with open("./conf/api_setup_params.yaml", 'r') as yaml_file:
    API_SETUP_PARAMS = yaml.safe_load(yaml_file)

# api version
with open("./env_spec/lsts_versions.yaml", 'r') as yaml_file:
    LSTS_VERSIONS = yaml.safe_load(yaml_file)

API_VERSION = LSTS_VERSIONS['api_version']

# read-in paramers values from env

PERSIST_FILEPATH = os.getenv("PERSIST_FILEPATH")
DATABASE_CONNECTOR_TYPE = os.getenv("DATABASE_CONNECTOR_TYPE")
BASE_URL_STRING = os.getenv("BASE_URL_STRING")
ACCESS_KEY = os.getenv("ACCESS_KEY")

# update default paramers if any env parameters were provided

if PERSIST_FILEPATH:
    MOCKER_SETUP_PARAMS['file_path'] = PERSIST_FILEPATH
if DATABASE_CONNECTOR_TYPE:
    API_SETUP_PARAMS['database_connector_type'] = DATABASE_CONNECTOR_TYPE
if BASE_URL_STRING:
    API_SETUP_PARAMS['base_url'] = BASE_URL_STRING
if ACCESS_KEY:
    API_SETUP_PARAMS['access_key'] = ACCESS_KEY



