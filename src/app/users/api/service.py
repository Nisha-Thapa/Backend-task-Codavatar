import math

from src.app import logs
from src.app.users.api.payload.response import UserList
from src.app.users.api.payload.request import UserCreateRequest, UserUpdateRequest
from src.app.users.repository import UserDataRepo


class UserService:
    def __init__(self):
        self._user_repo = UserDataRepo()

    async def get_users_list(self, pageIndex: int, pageSize: int):
        post_data = self._user_repo.fetch_all_users(pageIndex, pageSize)
        serializer = (
            UserList(users=post_data["data"])
            if post_data["data"]
            else UserList(users=[])
        )
        logs.info("Users Retrieval Completed")
        return {
            "page_index": post_data.get("page_index", 0),
            "page_size": post_data.get("page_size", 0),
            "total_pages": math.floor(post_data.get("total_pages", 0)),
            "total_records": post_data.get("total_records", 0),
            "serialized_data": serializer,
        }

    async def save_user(self, user_data: UserCreateRequest):
        self._user_repo.insert_user_data(user_data.__dict__)
        logs.info("User Creation Completed")
        return user_data

    async def update_user(self, user_data: UserUpdateRequest):
        updated_data = self._user_repo.update_user_data(user_data)
        logs.info("User Update Completed")
        return updated_data

    async def delete_user(self, user_id: int):
        self._user_repo.delete_user_data(user_id)
        logs.info("User Deletion Completed")
        return f"User with ID {user_id} deleted"
