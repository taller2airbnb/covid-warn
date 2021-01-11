from covidWarnApp.Errors.CovidWarnException import CovidWarnException
from flask import current_app

MESSAGE_DELTA_WINDOW_INVALID = "Number of days to calculate the delta of cases must be greater than 0."

MESSAGE_JUMPS_INVALID = "Number of days to calculate the jumps and total jumps must be greater than 1."

MESSAGE_FATALITY_DATA_INVALID = "Fatality rate date cant be negative"


class DeltaWindowInvalid(CovidWarnException):
    def __init__(self, message=MESSAGE_DELTA_WINDOW_INVALID):
        current_app.logger.error(MESSAGE_DELTA_WINDOW_INVALID)
        self.error_code = 409
        self.message = message
        super().__init__(self.message, self.error_code)


class JumpsInvalid(CovidWarnException):
    def __init__(self, message=MESSAGE_JUMPS_INVALID):
        current_app.logger.error(MESSAGE_JUMPS_INVALID)
        self.error_code = 409
        self.message = message
        super().__init__(self.message, self.error_code)


class FatalityRateDataInvalid(CovidWarnException):
    def __init__(self, message=MESSAGE_FATALITY_DATA_INVALID):
        current_app.logger.error(MESSAGE_FATALITY_DATA_INVALID)
        self.error_code = 409
        self.message = message
        super().__init__(self.message, self.error_code)