 import schedule
import time
import logging
from logs.log_config import setup_logging
from main import main

setup_logging()


def job():
    logging.info("Task running...")
    main()


job()

# Назначаем задачу на выполнение каждую минуту
schedule.every(15).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
