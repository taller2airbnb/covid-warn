from covidWarnApp.Errors.CovidWarnException import CovidWarnException
from flask import current_app


class DeltaWindowInvalid(CovidWarnException):
    def __init__(self, message="Number of days to calculate the delta of cases must be greater than 0."):
        current_app.logger.error("Number of days to calculate the delta of cases must be greater than 0.")
        self.error_code = 409
        self.message = message
        super().__init__(self.message, self.error_code)
