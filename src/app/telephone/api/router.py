from http import HTTPStatus
from datetime import datetime
from fastapi import APIRouter, status, Query
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from src.app import logs
from src.app.core.app_enum import ResponseCode
from src.app.core.app_schema import GenericResponse
from src.app.core.app_constants import APP_ROUTE_PREFIX
from src.app.telephone.api.service import TelephoneService
from src.app.telephone.api.payload.request import (
    VirtualPhoneNumberCreate,
    MakeCallRequest,
)

route_controller = APIRouter(prefix=APP_ROUTE_PREFIX)
telephone_service_obj = TelephoneService()


# PATH DEFINITIONS
@route_controller.post(
    path="/create-vir-num",
    tags=["Telephony"],
    summary="[CT-TP-01] Create the virtual number for a user",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse,
    description="""
        Create a virtual phone number for a user.

        Args:
            request (VirtualPhoneNumberCreate): Contains the virtual phone number details (phone number).
            user_id (int): The ID of the user to assign the virtual number to.

        Returns:
            Response: A JSONResponse with a success or failure message, and the created virtual number data if successful.

        Notes:
            - The `request` body should include the phone number.
            - The `user_id` is required as a query parameter to associate the virtual number with the user.
            - On success, the response includes the created virtual number.
            - On failure, an error message is returned.
    """,
)
async def create_virtual_number(
    request: VirtualPhoneNumberCreate,
    user_id: int = Query(),
):
    """Router Function for saving the vitrual number of a user"""
    # LOGS
    logs.info("Virtual NUmber Creation Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await telephone_service_obj.save_number(request, user_id)

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.CREATED
        respond.timeStamp = datetime.now()
        respond.message = "Virtual Number Created Successfully"
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
@route_controller.get(
    path="/vir-num",
    tags=["Telephony"],
    summary="[CT-TP-02] Get the list of the virtual Number of a user",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse,
    description="""
        Get a paginated list of virtual phone numbers associated with a user.

        Args:
            userID (int): The ID of the user whose virtual numbers are to be fetched.
            pageIndex (int): The page number of the result (default is 1).
            pageSize (int): The number of records per page (default is 5).

        Returns:
            Response: A JSONResponse with the list of virtual phone numbers, total records,
                    pagination details, and a success or failure message.

        Notes:
            - The `userID` is required as a query parameter to specify the user.
            - Pagination is handled with `pageIndex` and `pageSize` query parameters.
            - The response includes data about the virtual numbers, pagination details, and a success message.
            - On failure, an error message is returned.
    """,
)
async def get_phone_numbers(
    userID: int = Query(),
    pageIndex: int = Query(1, ge=1),
    pageSize: int = Query(5, ge=1),
):
    """Router Function for Retriving the Virtual Phone Number List"""
    # LOGS
    logs.info("Virtual Number Retrieval Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await telephone_service_obj.get_phone_number_list(
        userID, pageIndex, pageSize
    )

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.OK
        respond.timeStamp = datetime.now()
        respond.message = "User's Virtual Number Fetched Successfully"
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
@route_controller.get(
    path="/vir-num-li",
    tags=["Telephony"],
    summary="[CT-TP-03] Get the list of Virtual phone number and its associated Call logs",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse,
    description="""
        Retrieves the list of virtual phone numbers and their associated call logs.

        Args:
            pageIndex (int): The index of the page to retrieve (default: 1).
            pageSize (int): The number of records per page (default: 5).

        Returns:
            Response: A JSONResponse with the virtual phone number details and associated call logs.
            - `totalRecords`: The total number of records available.
            - `pageIndex`: The current page index.
            - `pageSize`: The number of records per page.
            - `totalPages`: The total number of pages based on `totalRecords` and `pageSize`.

        Notes:
            - The response includes detailed information for each virtual number, along with its associated call logs.
    """,
)
async def get_detail_list_phone_numbers(
    pageIndex: int = Query(1, ge=1),
    pageSize: int = Query(5, ge=1),
):
    """Router Function for Retriving the Virtual Phone Number List and Call Logs"""
    # LOGS
    logs.info("Virtual Number  List Retrieval Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await telephone_service_obj.get_detail_phone_number_list(
        pageIndex, pageSize
    )

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.OK
        respond.timeStamp = datetime.now()
        respond.message = "User's Virtual Number Fetched Successfully"
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
    path="/make-a-call",
    tags=["Telephony"],
    summary="[CT-TP-04] Saves the Call log whenever a call is made",
    status_code=status.HTTP_200_OK,
    response_model=GenericResponse,
    description="""
        Saves the call log whenever a virtual number makes a call.

        Args:
            request (MakeCallRequest):
                - source_number_id (int): The ID of the source virtual phone number making the call.
                - destination_phone_number (str): The phone number to which the call is being made.

        Returns:
            Response: A JSONResponse containing the success or failure status of the call log
                    creation along with the saved data.

        Notes:
            - The `source_number_id` is required to identify the virtual phone number that initiated the call.
            - The `destination_phone_number` must be a 10-digit number; if it is invalid, a validation error will be raised.
            - If the log is saved successfully, a success message is returned; otherwise, an error message is returned.
    """,
)
async def save_call_logs(
    request: MakeCallRequest,
):
    """Router Function for Saving the Call log of a virtual number"""
    # LOGS
    logs.info("Call Log Creation Started")

    # INITIALIZATIONS
    respond = GenericResponse

    # SERVICE-CALLS
    service_response = await telephone_service_obj.save_call_logs(request)

    # CASE CHECK [SUCCESS/FAILURE]
    if service_response is not None:
        respond.responseCode = ResponseCode.SUCCESS
        respond.httpStatusCode = HTTPStatus.OK
        respond.timeStamp = datetime.now()
        respond.message = "Call Log Saved Successfully"
        respond.data = service_response
    else:
        respond.responseCode = ResponseCode.FAILED
        respond.message = "ERROR: Failed to Save"

    # RETURNS
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(GenericResponse(**respond.__dict__).model_dump()),
    )
