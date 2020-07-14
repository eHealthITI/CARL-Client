class InvalidToken(Exception):
    """Error raised when the token is invalid"""

    def __init__(self) -> None:
        Exception.__init__(self)
        self.message = 'Invalid token! Please check your data!'


class PageNotFound(Exception):
    """Error raised when the page was not found i.e wrong endpoint url"""

    def __init__(self) -> None:
        Exception.__init__(self)
        self.message = 'Page not found!'


class CloudIsDown(Exception):
    """Error raised when the YpostirizoCloud is down"""

    def __init__(self) -> None:
        Exception.__init__(self)
        self.message = 'Ypostirizo Cloud seems to be down!'


class NotImplemented(Exception):
    """Error raised when the endpoint is not implemented"""

    def __init__(self) -> None:
        Exception.__init__(self)
        self.message = 'The method is not implemented. Make sure you are calling\
                        the right endpoint!'
