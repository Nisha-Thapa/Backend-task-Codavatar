from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from fastapi import status

from src.app import logs
from src.app.config.generic_config import GenericConfig
from src.app.core.database.data_connector import DBConnection
from src.app.util.utilities import get_or_404_not_found
import src.app.core.app_constants as _const

from src.app.core.exception.generic_app_exception import GenericAppException
from src.app.telephone.models import VirtualPhoneNumber, CallLog
from src.app.users.models import User


class TelephoneDataRepo:
    session: Session
    engine: Engine

    def __init__(self):
        configs = GenericConfig()
        config_details = configs.get_connection_details(_const.DATABASE_1)
        self.cursor, self.conn = DBConnection.get_db_connection_cursor(**config_details)
        self.session, self.engine = DBConnection.get_db_session_creator(
            **config_details
        )

    def check_user_existence(self, user_id: int):
        """Checks If User exist or not"""
        return get_or_404_not_found(User, user_id, self.session)

    def insert_telephone_number(self, data: dict, user: User):
        """Insert Virtual Number"""
        try:
            existing_number = (
                self.session.query(VirtualPhoneNumber)
                .filter(VirtualPhoneNumber.phone_number == data.get("phone_number"))
                .first()
            )
            if existing_number:
                raise GenericAppException(
                    status.HTTP_400_BAD_REQUEST,
                    "Phone number already exists.Choose Another Number.",
                )
            virtual_phone_number_data = VirtualPhoneNumber(
                phone_number=data.get("phone_number"), user_id=user.id
            )
            self.session.add(virtual_phone_number_data)
            self.session.commit()
            return virtual_phone_number_data
        except SQLAlchemyError as e:
            logs.error(f"Error inserting the virtual number data: {e}")
            self.session.rollback()
            raise GenericAppException(
                status.HTTP_400_BAD_REQUEST,
                f"Error: {e}]",
            )

    def fetch_user_numbers(
        self,
        user: User,
        page_index: int,
        page_size: int,
    ):
        """Fetch all user's Virtual Number"""
        try:
            query = self.session.query(VirtualPhoneNumber).filter(
                VirtualPhoneNumber.user_id == user.id
            )
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

    def fetch_all_virtual_numbers(
        self,
        page_index: int,
        page_size: int,
    ):
        """Fetch all Virtual Numbers"""
        try:
            query = self.session.query(VirtualPhoneNumber)
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
            logs.error(f"Error fetching Virtual Phone number lists: {e}")
            raise GenericAppException(
                status.HTTP_404_NOT_FOUND,
                f"Error: {e}",
            )

    def check_phone_number_existence(self, phone_id: int):
        """Checks If Virtual Phone Number exist or not"""
        return get_or_404_not_found(VirtualPhoneNumber, phone_id, self.session)

    def insert_call_logs(self, **kwargs):
        """Insert Virtual Number"""
        try:
            call_log = CallLog(
                phone_number_id=kwargs.get("source_phone_number").id,
                destination_phone_number=kwargs.get(
                    "phone_data"
                ).destination_phone_number,
                call_start_time=kwargs.get("start_time"),
                call_duration_seconds=kwargs.get("duration"),
                direction=kwargs.get("call_type"),
            )
            self.session.add(call_log)
            self.session.commit()
            return call_log
        except SQLAlchemyError as e:
            logs.error(f"Error inserting the call log: {e}")
            self.session.rollback()
            raise GenericAppException(
                status.HTTP_400_BAD_REQUEST,
                f"Error: {e}]",
            )
