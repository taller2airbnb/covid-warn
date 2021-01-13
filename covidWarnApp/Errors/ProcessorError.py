from covidWarnApp.Errors.CovidWarnException import CovidWarnException
from flask import current_app

MESSAGE_COUNTRY_INVALID = "Invalid Country"


class CountryInvalid(CovidWarnException):
    def __init__(self, message=MESSAGE_COUNTRY_INVALID):
        current_app.logger.error(MESSAGE_COUNTRY_INVALID)
        self.error_code = 409
        self.message = message
        super().__init__(self.message, self.error_code)