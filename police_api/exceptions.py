from requests.exceptions import HTTPError


class BaseException(Exception):
    pass


class APIError(BaseException, HTTPError):
    """
    The API responded with a non-200 status code.
    """

    def __init__(self, http_error):
        self.message = getattr(http_error, 'message', None)
        self.response = getattr(http_error, 'response', None)

    def __str__(self):
        return self.message or '<unknown error code>'


class InvalidCategoryException(BaseException):
    """
    The requested category was not found, or is unavailable for the given date.
    """
    pass
