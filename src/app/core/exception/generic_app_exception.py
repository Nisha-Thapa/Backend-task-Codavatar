from src.app import logs

from src.app.core.exception.app_runtime_exception import AppRuntimeException


class GenericAppException(AppRuntimeException):
    def __init__(
        self, errCode=1001, errMsg="Application Runtime Error occurred", ecp=None
    ):
        super().__init__(errCode, errMsg)
        if ecp is not None:
            logs.error(errMsg, exc_info=ecp)

    @classmethod
    def from_http_status(cls, status, errMsg):
        return cls(status.value, errMsg)
