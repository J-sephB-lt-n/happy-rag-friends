"""Functions for interacting with the database"""

import contextlib
import sqlite3

import pydantic

import config
from src.obj import Advisor


def sqlite_dict_factory(cursor, row):
    """Setting conn.row_factory=sqlite_dict_factory makes .fetchone(), .fetchall() etc. returning lists of dictionaries"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def create_advisor(
    advisor_name: str,
    personality_description: str,
    path_to_model: str,
):
    """Adds an advisor to the database"""
    try:
        advisor = Advisor(
            advisor_name=advisor_name,
            personality_description=personality_description,
            path_to_model=path_to_model,
        )
    except pydantic.ValidationError as error:
        return f"UNPROCESSABLE ENTITY\n{error}", 422

    with contextlib.closing(sqlite3.connect(config.DB_PATH)) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
            INSERT INTO advisors (advisor_name, personality_description, path_to_model)
            VALUES (?, ?, ?)
            ;
            """,
                (
                    advisor.advisor_name,
                    advisor.personality_description,
                    advisor.path_to_model,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            return "CONFLICT", 409
        return "OK", 200


def get_advisor_details():
    """Fetch basic info on every advisor in the database"""
    with contextlib.closing(sqlite3.connect(config.DB_PATH)) as conn:
        conn.row_factory = sqlite_dict_factory
        cursor = conn.cursor()
        advisors_info: list[dict] = cursor.execute(
            """                                                                     
            SELECT      advisor_name
                    ,   personality_description
                    ,   path_to_model
            FROM        advisors
            ;                                                                           
        """
        ).fetchall()
    return advisors_info
