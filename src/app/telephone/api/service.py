import math
import time
import random
from datetime import datetime


from src.app import logs
from src.app.telephone.api.payload.request import (
    VirtualPhoneNumberCreate,
    MakeCallRequest,
)
from src.app.telephone.api.payload.response import (
    VirtualNumberList,
    VirtualPhoneNumberResponse,
    CallLogResponse,
    VirtualPhoneNumberDetailList,
)
from src.app.telephone.repository import TelephoneDataRepo
from src.app.telephone.choices import CallType


class TelephoneService:
    def __init__(self):
        self._telephone_repo = TelephoneDataRepo()

    async def save_number(self, telephone_data: VirtualPhoneNumberCreate, user_id: int):
        user = self._telephone_repo.check_user_existence(user_id)
        telephone_data = self._telephone_repo.insert_telephone_number(
            telephone_data.__dict__, user
        )
        response_data = VirtualPhoneNumberResponse.model_validate(telephone_data)
        logs.info("Virtual Number Creation Completed")
        return response_data

    async def get_phone_number_list(
        self, user_id: int, page_index: int, page_size: int
    ):
        user = self._telephone_repo.check_user_existence(user_id)
        phone_numbers = self._telephone_repo.fetch_user_numbers(
            user, page_index, page_size
        )
        serializer = VirtualNumberList(
            id=user.id,
            name=user.name,
            email=user.email,
            mobile=user.mobile,
            address=user.address,
            gender=user.gender.value,
            phone_numbers=[num.phone_number for num in phone_numbers["data"]]
            if phone_numbers["data"]
            else [],
        )
        logs.info("Virtual Number Retrieval Completed")
        return {
            "page_index": phone_numbers.get("page_index", 0),
            "page_size": phone_numbers.get("page_size", 0),
            "total_pages": math.floor(phone_numbers.get("total_pages", 0)),
            "total_records": phone_numbers.get("total_records", 0),
            "serialized_data": serializer,
        }

    async def get_detail_phone_number_list(self, pageIndex: int, pageSize: int):
        phone_number_list = self._telephone_repo.fetch_all_virtual_numbers(
            pageIndex, pageSize
        )
        response_data = [
            VirtualPhoneNumberDetailList(
                id=number.id,
                phone_number=number.phone_number,
                user_name=number.owner.name,
                email=number.owner.email,
                call_logs=[
                    CallLogResponse.model_validate(log) for log in number.call_logs
                ],
            )
            for number in phone_number_list["data"]
        ]
        logs.info("Virtual Number List Retrieval Completed")
        return {
            "page_index": phone_number_list.get("page_index", 0),
            "page_size": phone_number_list.get("page_size", 0),
            "total_pages": math.floor(phone_number_list.get("total_pages", 0)),
            "total_records": phone_number_list.get("total_records", 0),
            "serialized_data": response_data,
        }

    async def save_call_logs(self, phone_data: MakeCallRequest):
        source_phone_number = self._telephone_repo.check_phone_number_existence(
            phone_data.source_number_id
        )
        start_dt = datetime.now()

        # Logic For Making a call starts here
        time.sleep(random.randint(0, 1))
        #
        end_dt = datetime.now()
        duration = int((end_dt - start_dt).total_seconds())

        call_log_data = self._telephone_repo.insert_call_logs(
            call_type=CallType.OUTGOING.value,
            phone_data=phone_data,
            source_phone_number=source_phone_number,
            start_time=start_dt,
            duration=duration,
        )
        call_log_response = CallLogResponse.model_validate(call_log_data)
        logs.info("Call Log Creation Completed")
        return call_log_response
