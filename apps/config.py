
import os
from dotenv import load_dotenv
import traceback
import sqlite3
import sqlalchemy


class Config(object):
    load_dotenv()
    BASEDIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
    print(f'base dir: {BASEDIR}')

    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_003')

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'chat_message.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 

   

