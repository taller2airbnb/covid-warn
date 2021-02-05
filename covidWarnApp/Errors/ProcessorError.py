from covidWarnApp.Errors.CovidWarnException import CovidWarnException
from flask import current_app

MESSAGE_COUNTRY_INVALID = "Invalid Country"
MESSAGE_EMPTY_DATA = "Sorry we have no data to process."
MESSAGE_CONNECTION_ABORTED = "Sorry the COVID API Server is currently unavailable. Please try again."


class CountryInvalid(CovidWarnException):
    def __init__(self, message=MESSAGE_COUNTRY_INVALID):
        current_app.logger.error(MESSAGE_COUNTRY_INVALID)
        self.error_code = 409
        self.message = message
        super().__init__(self.message, self.error_code)


class EmptyData(CovidWarnException):
    def __init__(self, message=MESSAGE_EMPTY_DATA):
        current_app.logger.error(MESSAGE_EMPTY_DATA)
        self.error_code = 409
        self.message = message
        super().__init__(self.message, self.error_code)


class ConnectionAborted(CovidWarnException):
    def __init__(self, message=MESSAGE_CONNECTION_ABORTED):
        current_app.logger.error(MESSAGE_CONNECTION_ABORTED)
        self.error_code = 404
        self.message = message
        super().__init__(self.message, self.error_code)
