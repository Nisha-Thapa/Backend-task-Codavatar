from src.app import logs


class AppRuntimeException(Exception):
    def __init__(self, errCode=1001, errMsg="Application Runtime Error occurred"):
        self.errorCode = errCode
        self.errorMsg = errMsg
        super().__init__(errMsg)
        logs.error(f"Error occurred: {errMsg}")

    def __str__(self):
        return f"AppRuntimeException: {self.errorMsg}"

    @classmethod
    def from_exception(cls, status, errMsg, exc):
        err = cls(status.value, errMsg)
        err.__cause__ = exc
        return err
