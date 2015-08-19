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
        self.status_code = getattr(self.response, 'status_code', None)

    def __str__(self):
        return self.message or '<unknown error code>'


class InvalidCategoryException(BaseException):
    """
    The requested category was not found, or is unavailable for the given date.
    """


class InvalidAPICallException(BaseException):
    """
    This is an API call that, due to limitations of the API, would be
    impossible to make.
    """


class NeighbourhoodsNeighbourhoodException(InvalidAPICallException):
    ("It is impossible to get information about the 'neighbourhoods' "
     "neighbourhood due to a conflict between "
     "https://data.police.uk/docs/method/neighbourhoods/ and "
     "https://data.police.uk/docs/method/neighbourhood/.")

    def __init__(self, *args, **kwargs):
        super(
            NeighbourhoodsNeighbourhoodException, self
        ).__init__(self.__doc__, *args, **kwargs)
