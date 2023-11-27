import os

from dotenv import load_dotenv

load_dotenv('.env.test')

assert os.getenv('ENV') == 'TEST'