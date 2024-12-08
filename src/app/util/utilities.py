from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import status, Query

from src.app import logs
from src.app.core.exception.generic_app_exception import GenericAppException


def get_or_404_not_found(qs, id: int, db: Session) -> Query:
    """
    Returns the object of the QuerySet provided on the basis of id else raises HTTPException 404

    Args:
        qs (class): Model from the models.py.
        id (int): Id of the model which uniquely defines the object.
        db (Session) : A session of database to perform database operations

    Returns:
        Response :A object that defines the model if available in the database
                else raises HTTPException for 404.
    """
    try:
        query = db.query(qs).filter(qs.id == id).first()
        if not query:
            logs.error("No data found")
            raise GenericAppException(
                status.HTTP_404_NOT_FOUND,
                f"{qs.__name__} instance not found",
            )
        return query
    except SQLAlchemyError as e:
        logs.error(f"Error: {e}")
        db.rollback()


def dictFromRow(row: dict) -> dict:
    """Generate Dictionary object from SQLAlchemy Row Object
    to use in Response body"""
    # INITIALIZATION
    data_row_dict = {}
    # OPERATIONS
    for item in row.__dict__:
        if not str(item).startswith("_"):
            data_row_dict[item] = row.__dict__[item]
    # RETURNS
    return data_row_dict
