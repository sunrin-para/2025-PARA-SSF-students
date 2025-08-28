from dotenv import load_dotenv
from .chat import *
from .playlist import *
from .user import *

env_path = ".env"
load_dotenv(dotenv_path=env_path) # env 파일을 불러옵니다.
