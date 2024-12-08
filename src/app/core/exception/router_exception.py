from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.app import logs
from src.app.core.app_enum import ResponseCode
from src.app.core.exception.app_runtime_exception import AppRuntimeException
from src.app.core.exception.generic_app_exception import GenericAppException

from src.app.core.app_schema import ErrorDetails, GenericResponse


def generateResponse(ecp: Exception) -> GenericResponse:
    """All Exception handling function"""
    response = GenericResponse()
    response.responseCode = ResponseCode.FAILED.value
    err_dtl = ErrorDetails()
    err_dtl.errorCode = ecp.errorCode if hasattr(ecp, "errorCode") else 500
    err_dtl.errorMessage = ecp.errorMsg if hasattr(ecp, "errorMsg") else str(ecp)
    response.errorDetails = []
    response.errorDetails.append(err_dtl)
    response.httpStatusCode = ecp.errorCode if hasattr(ecp, "errorCode") else 500
    response.timeStamp = datetime.now()
    return response


def initiate_exception_handling(app_route_avatar: FastAPI):
    """INITIALIZES ALL EXCEPTION TYPE & RESPONSES"""

    logs.info(" ROUTER-CT: EXCEPTION HANDLERS INITIALIZED ")

    @app_route_avatar.exception_handler(AppRuntimeException)
    async def app_runtime_exception_handler(request: Request, exc: AppRuntimeException):
        """Exception handler for Application Runtime Errors"""
        response = generateResponse(exc)
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(GenericResponse(**response.__dict__).model_dump()),
        )

    @app_route_avatar.exception_handler(FileNotFoundError)
    async def file_not_found_exception_handler(
        request: Request, exc: FileNotFoundError
    ):
        """Exception handler for Missing File Errors"""
        response = generateResponse(exc)
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(GenericResponse(**response.__dict__).model_dump()),
        )

    @app_route_avatar.exception_handler(GenericAppException)
    async def generic_app_exception_handler(request: Request, exc: GenericAppException):
        """Exception handler for All Generic Application Exceptions"""
        response = generateResponse(exc)
        return JSONResponse(
            status_code=exc.errorCode,
            content=jsonable_encoder(GenericResponse(**response.__dict__).model_dump()),
        )

    @app_route_avatar.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        request: Request, exc: RequestValidationError
    ):
        """Exception handler for FastAPI Request Validation Errors"""
        error_details = [
            ErrorDetails(
                errorCode=status.HTTP_400_BAD_REQUEST,
                errorMessage=f"{error['loc'][-1]}: {error['msg']}",
            )
            for error in exc.errors()
        ]
        response = GenericResponse(
            responseCode=ResponseCode.FAILED.value,
            httpStatusCode=status.HTTP_400_BAD_REQUEST,
            errorDetails=error_details,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(response.model_dump()),
        )
