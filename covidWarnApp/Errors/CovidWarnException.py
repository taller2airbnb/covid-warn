class CovidWarnException(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, message, error_code=400):
        self.message = message
        self.error_code = error_code

