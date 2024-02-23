import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='app.log',  # Указываете путь к файлу лога
        filemode='a'  # 'a' для добавления к существующему содержимому, 'w' для перезаписи файла
    )
