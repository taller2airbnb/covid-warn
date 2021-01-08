from covidWarnApp.Errors import ParamsError


def validate_number_days_window_delta(days):
    if days <= 0:
        raise ParamsError.DeltaWindowInvalid
