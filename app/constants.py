import re
from os import environ as env

from dotenv import load_dotenv

ENV = env.get('ENV')

if ENV == 'TEST':
    load_dotenv('.env.test')
else:
    load_dotenv('.env')

FILE_PATH = 'app/data'

ABBREVIATIONS_FILE_NAME = 'abbreviations.txt'
START_FILE_NAME = 'start.txt'
END_FILE_NAME = 'end.txt'
STAGE_FILE_NAME = 'stages.txt'

ABBREVIATIONS = f'{FILE_PATH}/{ABBREVIATIONS_FILE_NAME}'
START = f'{FILE_PATH}/{START_FILE_NAME}'
END = f'{FILE_PATH}/{END_FILE_NAME}'
STAGES = f'{FILE_PATH}/{STAGE_FILE_NAME}'

TIME_FORMAT = '%Y-%m-%d_%H:%M:%S.%f'
PATTERN = re.compile(
    r'([A-Z]*)(\d{4}-\d{2}-\d{2}_\d{2}:\d{2}:\d{2}.\d{3})'
)

DB_NAME = env.get('DB_NAME')
DB_PASSWORD = env.get('DB_PASSWORD')
DB_USER = env.get('DB_USER')
DB_PORT = env.get('DB_PORT')
DB_HOST = env.get('DB_HOST')
DB_ENGINE = env.get('DB_ENGINE')
RUN_HOST = env.get('RUN_HOST')
RUN_PORT = env.get('RUN_PORT')
RUN_DEBUG = env.get('RUN_DEBUG')

DB_POSTGRES = env.get('DB_SUPERUSER')

DB_BASE_URL = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'

ECHO_OPTIONS = {'echo': True}
