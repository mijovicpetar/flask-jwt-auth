"""Exceptions module."""


API_BAD_DATA = 400
API_UNPROCESSABLE_ENTITY = 422
API_INTERNAL_ERROR = 500

class ApiException(Exception):
    """Exception for handling API call exceptions."""

    def __init__(self, message: str, status: int):
        """API Exception init.

        Args:
            message (str): Error message.
            status (int): API status code.
        """
        self.status = status
        self.message = message
        super().__init__(self.message)


class BadDataApiException(ApiException):
    def __init__(self, message: str):
        self.status = API_BAD_DATA
        self.message = message
        super().__init__(self.message, self.status)


class InternalErrorApiException(ApiException):
    def __init__(self, message: str):
        self.status = API_INTERNAL_ERROR
        self.message = message
        super().__init__(self.message, self.status)
