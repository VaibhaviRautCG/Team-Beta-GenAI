
import os
from dotenv import load_dotenv
import traceback

class Config(object):
    load_dotenv()
    BASEDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    print(f'base dir: {BASEDIR}')

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_003')

    OPENAI_API_KEY = os.getenv('OPENAI.API_KEY')
    pass