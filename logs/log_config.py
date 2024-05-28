import logging
from dotenv import load_dotenv
import os

load_dotenv()
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=LOG_FILE_PATH,
        filemode='a'  # 'a' для добавления к существующему содержимому, 'w' для перезаписи файла
    )
