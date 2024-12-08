""" Connection to wire in with the database
and access the Database services """

import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.app import logs

Base = declarative_base()


class DBConnection:
    @staticmethod
    def get_db_connection_cursor(host, username, password, port, database, **kwargs):
        """gets db connection cursor"""
        try:
            conn = psycopg2.connect(
                host=host, user=username, password=password, port=port, dbname=database
            )
            cursor = conn.cursor()
            return cursor, conn

        except psycopg2.Error as err:
            logs.error(f"unable to establish engine connection-- {err}")

    @staticmethod
    def get_db_session_creator(
        driver_name, username, password, host, port, database, **kwargs
    ):
        """Create the DB with the proper connection details"""
        session_object = None
        engine = None
        try:
            engine = create_engine(
                sqlalchemy.engine.URL.create(
                    drivername=driver_name,
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                    database=database,
                )
            )
        except exc.SQLAlchemyError as err:
            logs.error(f"unable to establish engine connection-{err}")
        try:
            session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            session_object = session_local()
        except exc.SQLAlchemyError as e:
            logs.error(40, f"unable to establish session-{e}")

        # Return connections
        return session_object, engine
