import psycopg2
import logging
from api_server.config import *

def create_db_connection(db_name = None):

    if db_name is None:
        db_name = DATABASE_NAME
    logging.info(f'Connecting to a database {db_name}...')
    conn = psycopg2.connect(
        host = DATABASE_HOST,
        port = DATABASE_PORT,
        dbname = db_name,
        user = DATABASE_USER,
        password = DATABASE_PASSWORD)
    logging.info(f'Connected to a database {db_name}')
    return conn

def init_db():

    logging.info('Starting database initialization and migration...')

    # Connecting as a superuser to a main postgres database
    try:
        conn = create_db_connection('postgres')
    except Exception:
        logging.exception('Error while connecting to a main postgres database. Terminating process...')
        exit()
    conn.autocommit = True
    curs = conn.cursor()

    # Executing queries to delete our database if exists and create a new one
    try:    
        curs.execute('DROP DATABASE IF EXISTS "dtse-assignment-task-db";')
        curs.execute('CREATE DATABASE "dtse-assignment-task-db" WITH TEMPLATE = template0 ENCODING = \'UTF8\';')
    except Exception:
        logging.exception('Error while creating database. Terminating process...')
        curs.close()
        conn.close()
        exit()

    curs.close()
    conn.close()

    # Opening a new connection to a our database
    try:
        conn = create_db_connection()
    except Exception:
        logging.exception('Error while connecting to a database. Terminating process...')
        exit()
    conn.autocommit = True
    curs = conn.cursor()

    logging.info('Backuping database structure...')

    # Reading all contents of backup file
    f = open('db_backup.sql', 'r')
    try:
        # Executing backup query
        curs.execute(f.read())
    except Exception:
        logging.exception('Error while backuping database. Terminating process...')
        curs.close()
        conn.close()
        exit()

    curs.close()
    conn.close()

    logging.info('Database was successfully initializated')