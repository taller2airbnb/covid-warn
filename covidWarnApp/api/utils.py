from covidWarnApp.Errors import ParamsError


def validate_number_days_window_delta(days):
    if days <= 0:
        raise ParamsError.DeltaWindowInvalid


def validate_number_jump_days(days):
    if days <= 1:
        raise ParamsError.JumpsInvalid


def validate_number_jumps(jumps):
    if jumps <= 1:
        raise ParamsError.JumpsInvalid


def validate_fatality_rate_data(rate):
    if rate < 0:
        raise ParamsError.FatalityRateDataInvalidd
