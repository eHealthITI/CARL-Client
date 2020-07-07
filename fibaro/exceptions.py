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
