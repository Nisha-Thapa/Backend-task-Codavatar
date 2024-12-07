#!usr/bin/python3

""" Generic Models for request and response """
from datetime import datetime
from http import HTTPStatus
from typing import Generic, TypeVar

from pydantic import BaseModel

from src.app.core.app_enum import ResponseCode

# Type Definition for Generalization
T = TypeVar("T")


class GenericRequest(BaseModel, Generic[T]):
    data: T
    pageIndex: int | None = 1
    pageSize: int | None = 100


class ErrorDetails(BaseModel):
    errorCode: int = None
    errorMessage: str = None


# class GenericError(BaseModel):
#     errorsList: list[ErrorDetails] = []


class GenericResponse(BaseModel, Generic[T]):
    responseCode: ResponseCode | None = None
    httpStatusCode: HTTPStatus | None = None
    message: str | None = None
    timeStamp: datetime | None = None
    errorDetails: list[ErrorDetails] | None = None
    data: T | None = None
    totalRecords: int | None = 0
    pageIndex: int | None = 0
    pageSize: int | None = 0
    totalPages: int | None = 0
