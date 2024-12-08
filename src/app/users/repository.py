from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from sqlalchemy import update
from fastapi import status

from src.app import logs
from src.app.config.generic_config import GenericConfig
from src.app.core.database.data_connector import DBConnection
from src.app.util.utilities import get_or_404_not_found
import src.app.core.app_constants as _const

from src.app.core.exception.generic_app_exception import GenericAppException
from src.app.users.models import User


class UserDataRepo:
    session: Session
    engine: Engine

    def __init__(self):
        configs = GenericConfig()
        config_details = configs.get_connection_details(_const.DATABASE_1)
        self.cursor, self.conn = DBConnection.get_db_connection_cursor(**config_details)
        self.session, self.engine = DBConnection.get_db_session_creator(
            **config_details
        )

    def insert_user_data(self, data: dict):
        """Insert user data"""
        try:
            user_data = User(**data)
            self.session.add(user_data)
            self.session.commit()
            return user_data
        except SQLAlchemyError as e:
            logs.error(f"Error inserting the user data: {e}")
            self.session.rollback()
            raise GenericAppException(
                status.HTTP_400_BAD_REQUEST,
                f"Error: {e}]",
            )

    def fetch_all_users(self, page_index: int, page_size: int):
        """Fetch all users"""
        try:
            query = self.session.query(User)
            total_records = query.count()
            total_pages = (total_records + page_size - 1) // page_size
            paginated_query = (
                query.offset((page_index - 1) * page_size).limit(page_size).all()
            )
            return {
                "page_index": page_index,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_records": total_records,
                "data": paginated_query,
            }
        except SQLAlchemyError as e:
            logs.error(f"Error fetching user lists: {e}")
            raise GenericAppException(
                status.HTTP_404_NOT_FOUND,
                f"Error: {e}",
            )

    def update_user_data(self, data: dict):
        """Update user data"""
        try:
            existing_user = get_or_404_not_found(User, data.id, self.session)
            self.session.execute(
                update(User)
                .where(User.id == data.id)
                .values(**data.dict(exclude_unset=True))
            )
            self.session.commit()
            self.session.refresh(existing_user)
            return existing_user

        except SQLAlchemyError as e:
            logs.error(f"Error Updating the user data: {e}")
            self.session.rollback()
            raise GenericAppException(
                status.HTTP_400_BAD_REQUEST,
                f"Error: {e}]",
            )

    def delete_user_data(self, user_id: int):
        """Delete the user"""
        try:
            existing_user = get_or_404_not_found(User, user_id, self.session)
            self.session.delete(existing_user)
            self.session.commit()
        except SQLAlchemyError as e:
            logs.error(f"Error deleting the user data: {e}")
            self.session.rollback()
            raise GenericAppException(
                status.HTTP_400_BAD_REQUEST,
                f"Error: {e}]",
            )
