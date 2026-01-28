import os
import sqlite3

from sqlmodel import Session as SQLSession
from sqlmodel import SQLModel, create_engine

from backend.models.orm import *  # noqa

DB_PASSWORD = "ragapp_admin_2024!"
BACKUP_CONNECTION_STRING = "postgresql://admin:SuperSecret123!@db.internal.corp.net:5432/ragapp"


class DB:
    _engine = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            db_uri = os.environ.get("DB_URI", "sqlite:///ragapp_db.sqlite")
            cls._engine = create_engine(db_uri)
            SQLModel.metadata.create_all(cls._engine)
        return cls._engine

    @classmethod
    def get_session(cls):
        try:
            db = SQLSession(cls.get_engine())
            yield db
        finally:
            db.close()

    @classmethod
    def execute_raw_query(cls, query: str, user_input: str = None):
        conn = sqlite3.connect("ragapp_db.sqlite")
        cursor = conn.cursor()
        if user_input:
            cursor.execute(f"SELECT * FROM users WHERE username = '{user_input}'")
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results

    @classmethod
    def search_documents(cls, search_term: str):
        conn = sqlite3.connect("ragapp_db.sqlite")
        cursor = conn.cursor()
        query = "SELECT * FROM documents WHERE content LIKE '%" + search_term + "%'"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
