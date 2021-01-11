from scipy.stats import linregress
from covidWarnApp.model import RulesParams
import datetime
import requests
import pandas as pd
from covidWarnApp.api import COVID_API


# Si fatality rate sube, se esta subtesteando, hay mas casos de lo que se cree.
# jump days cada cuantos dias sacas una foto (mirando pa atras)

def process_means(country, number_days_window, jump_days, total_jumps):
    my_populated_list = populate_list(number_days_window, country)
    means_list = []
    fatality_rate = []
    active_cases = []
    total_lapse_day = jump_days * total_jumps
    df = pd.DataFrame(my_populated_list,
                      columns=['day-number', 'active', 'cases-count', 'delta', 'fatality_rate', 'date'])

    for n in range(total_lapse_day, 0, -jump_days):
        try:
            mean = round(df[-(n):-(n - (jump_days))]['delta'].mean())
            active = round(df[-(n):-(n - (jump_days))]['active'].mean())
        except:
            mean = round(df[-(n):-(n - (jump_days - 1))]['delta'].mean())
            active = round(df[-(n):-(n - (jump_days - 1))]['active'].mean())
        means_list.append(mean)
        fatality_rate.append(df[-n:-(n - 1)]['fatality_rate'].mean())
        active_cases.append(active)
    return means_list, fatality_rate, active_cases


def populate_list(number_days_window, country):
    populated_list = []
    all_days = request_all_days_from_country(country)
    first = True
    for day in all_days.json():
        date_time_obj = datetime.datetime.strptime(day['Date'][:10], '%Y-%m-%d')
        if first:
            ordinal_first = date_time_obj.toordinal()
        n = date_time_obj.toordinal() - ordinal_first
        delta = 0
        fatality_rate = 0
        if n > number_days_window:
            delta = (day['Confirmed'] - populated_list[n - number_days_window][2]) / number_days_window
        first = False
        if day['Confirmed'] > 0:
            fatality_rate = day['Deaths'] / day['Confirmed']
        populated_list.append((n, day['Active'], day['Confirmed'], delta, fatality_rate, date_time_obj))
    return populated_list


def request_all_days_from_country(country):
    try:
        all_days = requests.get(COVID_API + country)
    except:
        all_days = requests.get(COVID_API + country, verify=False)
    return all_days


class Processor:
    def __init__(self, country):
        self.country = country
        self.number_days_window_delta = RulesParams.query.first().number_days_window_delta
        self.jump_days = RulesParams.query.first().jump_days
        self.total_jumps = RulesParams.query.first().total_jumps
        self.means_list = []
        self.means_list_slope = ''
        self.fatality_rate = []
        self.fatality_rate_range = 'between range'
        self.fatality_rate_slope = ''
        self.active_cases = []
        self.active_cases_slope = ''
        self.rep_means_list_slope = ''
        self.threshold_slope_variation = RulesParams.query.first().threshold_slope_variation

    def process(self):
        means_list, fatality_rate, active_cases = process_means(self.country, self.number_days_window_delta,
                                                                self.jump_days, self.total_jumps)
        self.means_list = means_list
        self.fatality_rate = fatality_rate
        self.active_cases = active_cases

        self.__process_delta_means()
        self.__process_active_cases()
        self.__process_fatality_rates()

    def __process_delta_means(self):
        total_jumps = self.total_jumps
        val_means_list_slope = linregress(range(total_jumps), self.means_list)[0]
        self.means_list_slope = "positive" if val_means_list_slope > 0 else "negative"
        rep_means_list_slope = val_means_list_slope / (sum(self.means_list) / total_jumps)
        self.rep_means_list_slope = "stable" if (rep_means_list_slope < self.threshold_slope_variation) else "unstable"

    def __process_fatality_rates(self):
        total_jumps = self.total_jumps
        rule_fatality_rate = RulesParams.query.first().fatality_rate
        fatality_rate_variation = RulesParams.query.first().fatality_rate_variation
        min_fatality_rate = rule_fatality_rate - fatality_rate_variation
        max_fatality_rate = rule_fatality_rate + fatality_rate_variation

        self.fatality_rate_slope = "positive" if linregress(range(total_jumps), self.fatality_rate)[
                                                     0] > 0 else "negative"

        if not (min_fatality_rate < self.fatality_rate[-1] < max_fatality_rate):
            self.fatality_rate_range = "under" if self.fatality_rate[-1] < rule_fatality_rate else "above"

    def __process_active_cases(self):
        total_jumps = self.total_jumps

        self.active_cases_slope = "positive" if linregress(range(total_jumps), self.active_cases)[0] > 0 else "negative"
