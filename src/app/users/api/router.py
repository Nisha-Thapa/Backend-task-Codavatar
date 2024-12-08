from http import HTTPStatus
from datetime import datetime
from fastapi import APIRouter, status, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.app import logs
from src.app.core.app_enum import ResponseCode
from src.app.core.app_schema import GenericRequest
from src.app.core.app_schema import GenericResponse
from src.app.core.app_constants import APP_ROUTE_PREFIX
from src.app.users.api.service import UserService
from src.app.users.api.payload.request import UserCreateRequest, UserUpdateRequest

route_controller = APIRouter(prefix=APP_ROUTE_PREFIX)
user_service_obj = UserService()


# PATH DEFINITIONS
@route_controller.get(
    path="/users",
    tags=["Users"],
    summary="[CT-UMS-01] Get the list of the Users",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse,
    description="""
        Get a paginated list of users from the database.

        Args:
            pageIndex (int): The page number to fetch. The default value is 1.
            pageSize (int): The number of users to display per page. The default value is 5.

        Returns:
            Response: A JSONResponse that contains the message about successful retrieval of user data,
                    along with the paginated list of users and metadata like total records, total pages,
                    and current page information.
    """,
)
async def get_user_data(
    pageIndex: int = Query(1, ge=1),
    pageSize: int = Query(5, ge=1),
):
    """Router Function for Retriving the User Lists"""
    # LOGS
    logs.info("Users Retrieval Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await user_service_obj.get_users_list(pageIndex, pageSize)

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.OK
        respond.timeStamp = datetime.now()
        respond.message = "Users Fetched Successfully"
        respond.data = service_response["serialized_data"]
        respond.totalRecords = service_response["total_records"]
        respond.pageIndex = service_response["page_index"]
        respond.pageSize = service_response["page_size"]
        respond.totalPages = service_response["total_pages"]
    else:
        respond.responseCode = ResponseCode.FAILED
        respond.message = "ERROR: Failed to Retrieved"

    # RETURNS
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(GenericResponse(**respond.__dict__).model_dump()),
    )


# PATH DEFINITIONS
@route_controller.post(
    path="/create-user",
    tags=["Users"],
    summary="[CT-UMS-02] Create a User",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse,
    description="""
    Create a new user and save their data.

        Args:
            request (UserCreateRequest): Contains user data: name, email, address, and gender.

        Returns:
            Response: A JSONResponse with a success or failure message, and the saved user data if successful.

        Notes:
            - The request body should include user details for creation.
            - On success, the response includes the saved user data.
            - On failure, an error message is returned.
    """,
)
async def create_user(
    request: GenericRequest[UserCreateRequest],
):
    """Router Function for saving the user data"""
    # LOGS
    logs.info("User Creation Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await user_service_obj.save_user(request.data)

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.CREATED
        respond.timeStamp = datetime.now()
        respond.message = "User Created Successfully"
        respond.data = service_response
    else:
        respond.responseCode = ResponseCode.FAILED
        respond.message = "ERROR: Failed to Save"

    # RETURNS
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(GenericResponse(**respond.__dict__).model_dump()),
    )


# PATH DEFINITIONS
@route_controller.patch(
    path="/update",
    tags=["Users"],
    summary="[CT-UMS-03] Update the User",
    status_code=200,
    response_model=GenericResponse,
    description="""
        Update an existing user’s data.

        Args:
            request (UserUpdateRequest): Contains the updated user details.

        Returns:
            Response: A JSONResponse with a success or failure message, and the updated user data if successful.

        Notes:
            - The request body should include the updated user details.
            - On success, the response includes the updated user data.
            - On failure, an error message is returned.
    """,
)
async def update_user(
    request: GenericRequest[UserUpdateRequest],
):
    """Router Function for updating the users"""
    # LOGS
    logs.info("User Update service Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await user_service_obj.update_user(request.data)

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.OK
        respond.timeStamp = datetime.now()
        respond.message = "User Updated Successfully"
        respond.data = service_response
    else:
        respond.responseCode = ResponseCode.FAILED
        respond.message = "ERROR: Failed to Update"

    # RETURNS
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(GenericResponse(**respond.__dict__).model_dump()),
    )


# PATH DEFINITIONS
@route_controller.delete(
    path="/delete",
    tags=["Users"],
    summary="[CT-UMS-04] Dalete the User",
    status_code=200,
    response_model=GenericResponse,
    description="""
        Delete an existing user by their ID.

        Args:
            user_id (int): The ID of the user to be deleted.

        Returns:
            Response: A JSONResponse with a success or failure message.

        Notes:
            - The `user_id` query parameter should specify the user to delete.
            - On success, the response confirms the user deletion.
            - On failure, an error message is returned.
    """,
)
async def delete_user(
    user_id: int = Query(),
):
    """Router Function for updating the users"""
    # LOGS
    logs.info("User Deletion Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await user_service_obj.delete_user(user_id)

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.OK
        respond.timeStamp = datetime.now()
        respond.message = "User Deleted Successfully"
        respond.data = service_response
    else:
        respond.responseCode = ResponseCode.FAILED
        respond.message = "ERROR: Failed to Delete"

    # RETURNS
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(GenericResponse(**respond.__dict__).model_dump()),
    )
