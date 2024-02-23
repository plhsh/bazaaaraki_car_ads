import psycopg2
from contextlib import contextmanager
from logs.log_config import setup_logging
import logging

setup_logging()


class Database:
    def __init__(self, dbname, user, password, host='localhost'):
        self.conn = None
        self.cur = None
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host
        }

    @contextmanager
    def database_cursor(self):
        try:
            self.connect()
            yield self.cur
            logging.info("Operation with database cursor completed successfully.")
        finally:
            self.close()

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            self.cur = self.conn.cursor()
            logging.info("Database connection established.")
        except Exception as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise

    def close(self):
        try:
            self.cur.close()
            self.conn.close()
            logging.info("Database connection closed.")
        except Exception as e:
            logging.error(f"Failed to close the database connection: {e}")

    def create_table(self):
        try:
            with self.database_cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS baz_car_ads (
                                id SERIAL PRIMARY KEY,
                                ad_id TEXT UNIQUE NOT NULL,
                                title TEXT NOT NULL,
                                year INT,
                                price INT,
                                milage INT,
                                transmission TEXT,
                                engine_type TEXT,
                                location_1 TEXT,
                                location_2 TEXT,
                                date TEXT,
                                url TEXT UNIQUE,
                                ad_active BOOLEAN DEFAULT TRUE
                            );
                        """)
                self.conn.commit()
                logging.info("Table created successfully.")
        except Exception as e:
            logging.error(f"An error occurred while creating the table: {e}")

    def update_ads_active_status(self, active_ads_ids):
        """Обновляет статус активности объявлений на основе списка активных ad_id."""
        # Преобразование списка ID в строку для SQL запроса
        active_ids_str = ','.join(f"'{ad_id}'" for ad_id in active_ads_ids)

        try:
            with self.database_cursor() as cursor:
                # Обновляем все объявления, чьи ad_id не находятся в списке активных, как неактивные
                cursor.execute(f"UPDATE baz_car_ads SET ad_active = FALSE WHERE ad_id NOT IN ({active_ids_str});")
                self.conn.commit()
        except Exception as e:
            logging.error(f"An error occurred while updating ads active status: {e}")
            if self.conn and not self.conn.closed:
                self.conn.rollback()

    def insert_or_update_ads_to_db(self, ads):
        """Вставляет или обновляет данные объявлений в базе данных, отмечая активные объявления."""
        # Собираем список ad_id для всех передаваемых объявлений
        active_ads_ids = [ad.id for ad in ads]

        insert_query = """
              INSERT INTO baz_car_ads (ad_id, title, year, price, milage, transmission, engine_type, location_1, location_2, date, url, ad_active)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
              ON CONFLICT (ad_id) 
              DO UPDATE SET
                  title = EXCLUDED.title,
                  year = EXCLUDED.year,
                  price = EXCLUDED.price,
                  milage = EXCLUDED.milage,
                  transmission = EXCLUDED.transmission,
                  engine_type = EXCLUDED.engine_type,
                  location_1 = EXCLUDED.location_1,
                  location_2 = EXCLUDED.location_2,
                  date = EXCLUDED.date,
                  url = EXCLUDED.url,
                  ad_active = TRUE;  -- Обновление ad_active до TRUE для активных объявлений
          """
        try:
            with self.database_cursor() as cursor:
                for ad in ads:
                    cursor.execute(insert_query, (
                        ad.id, ad.title, ad.year, ad.price, ad.milage, ad.transmission, ad.engine_type, ad.location_1,
                        ad.location_2, ad.date, ad.url))
                self.conn.commit()
                logging.info(f"{len(ads)} ads inserted/updated in the database.")
        except Exception as e:
            logging.error(f"An error occurred while inserting/updating ads to the database: {e}")
            if self.conn and not self.conn.closed:
                self.conn.rollback()

        # После обновления/вставки всех объявлений, обновляем статус активности
        self.update_ads_active_status(active_ads_ids)


