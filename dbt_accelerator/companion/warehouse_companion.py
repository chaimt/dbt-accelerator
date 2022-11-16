import logging
import os

import snowflake.connector

from dbt_accelerator.companion.common_companion import CompanionBase

logger = logging.getLogger(__name__)


class WarehouseCompanion(CompanionBase):

    def __init__(self):
        self.credentials = {
            'account'    : 'gza46147'
            , 'user'     : os.environ["SNOWFLAKE_USER"]
            , 'authenticator' : 'externalbrowser'
            }        

    def get_version(self) -> str:
        with snowflake.connector.connect(**self.credentials) as cnx:
            cur  = cnx.cursor()
            cur.execute("SELECT current_version()")
            text = cur.fetchall()   
            return text
        

    def setup_user_db(self):
        # Gets the version
        db_name = "dev_chaim"
        with snowflake.connector.connect(**self.credentials) as cnx:
            cur  = cnx.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            cur.execute(f"USE DATABASE {db_name}")
            cur.execute("CREATE SCHEMA IF NOT EXISTS myschema")
            
        logger.info(f"Created DB {db_name}")

    def clean_user_database(self):
        db_name = "dev_chaim"
        with snowflake.connector.connect(**self.credentials) as cnx:
            cur  = cnx.cursor()
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
        logger.info(f"Droped DB {db_name}")
