from scipy.stats import linregress

from covidWarnApp.Errors import ProcessorError
from covidWarnApp.model import RulesParams
import datetime
import requests
import pandas as pd
from covidWarnApp.api import COVID_API


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
        self.variation_means_list_slope = ''
        self.threshold_slope_variation = RulesParams.query.first().threshold_slope_variation

    def process(self):
        means_list, fatality_rate, active_cases = self.__process_means(self.country, self.number_days_window_delta,
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
        print("con", val_means_list_slope)
        self.means_list_slope = "positive" if val_means_list_slope > 0 else "negative"
        rep_means_list_slope = val_means_list_slope / (sum(self.means_list) / total_jumps)
        self.variation_means_list_slope = "stable" if (
                rep_means_list_slope < self.threshold_slope_variation) else "unstable"
        if rep_means_list_slope >= self.threshold_slope_variation * 3:
            self.variation_means_list_slope = "tripling"

    def __process_fatality_rates(self):
        total_jumps = self.total_jumps
        rule_fatality_rate = RulesParams.query.first().fatality_rate / 100
        fatality_rate_variation = RulesParams.query.first().fatality_rate_variation / 100
        min_fatality_rate = rule_fatality_rate - fatality_rate_variation
        max_fatality_rate = rule_fatality_rate + fatality_rate_variation

        self.fatality_rate_slope = "positive" if linregress(range(total_jumps), self.fatality_rate)[
                                                     0] > 0 else "negative"

        if not (min_fatality_rate < self.fatality_rate[-1] < max_fatality_rate):
            print(min_fatality_rate, self.fatality_rate[-1], max_fatality_rate)
            self.fatality_rate_range = "under" if self.fatality_rate[-1] < rule_fatality_rate else "above"

    def __process_active_cases(self):
        total_jumps = self.total_jumps
        val_active_cases_slope = linregress(range(total_jumps), self.active_cases)[0]
        print("ac", val_active_cases_slope)
        self.active_cases_slope = "positive" if val_active_cases_slope > 0 else "negative"

    def __process_means(self, country, number_days_window, jump_days, total_jumps):
        my_populated_list = self.__populate_list(number_days_window, country)
        means_list = []
        fatality_rate = []
        active_cases = []
        total_lapse_day = jump_days * total_jumps
        df = pd.DataFrame(my_populated_list,
                          columns=['day-number', 'active', 'cases-count', 'delta_confirmed', 'fatality_rate', 'date',
                                   'delta_active'])

        for n in range(total_lapse_day, 0, -jump_days):
            try:
                mean = round(df[-(n):-(n - (jump_days))]['delta_confirmed'].mean())
                active = round(df[-(n):-(n - (jump_days))]['delta_active'].mean())
            except:
                mean = round(df[-(n):-(n - (jump_days - 1))]['delta_confirmed'].mean())
                active = round(df[-(n):-(n - (jump_days - 1))]['delta_active'].mean())
            means_list.append(mean)
            fatality_rate.append(df[-n:-(n - 1)]['fatality_rate'].mean())
            active_cases.append(active)
        return means_list, fatality_rate, active_cases

    def __populate_list(self, number_days_window, country):
        populated_list = []
        all_days = self.__request_all_days_from_country(country)
        first = True
        for day in all_days.json():
            date_time_obj = datetime.datetime.strptime(day['Date'][:10], '%Y-%m-%d')
            if first:
                ordinal_first = date_time_obj.toordinal()
            n = date_time_obj.toordinal() - ordinal_first
            delta_confirmed = 0
            delta_active = 0
            fatality_rate = 0
            if n > number_days_window:
                delta_confirmed = (day['Confirmed'] - populated_list[n - number_days_window][2]) / number_days_window
                delta_active = (day['Active'] - populated_list[n - number_days_window][1]) / number_days_window
            first = False
            if day['Confirmed'] > 0:
                fatality_rate = day['Deaths'] / day['Confirmed']
            populated_list.append((n, day['Active'], day['Confirmed'], delta_confirmed, fatality_rate, date_time_obj,
                                   delta_active))
        return populated_list

    def __request_all_days_from_country(self, country):
        try:
            all_days = requests.get(COVID_API + country)
        except requests.exceptions.SSLError:
            all_days = requests.get(COVID_API + country, verify=False)
        validate_response_from_api(all_days)
        self.country = all_days.json()[0]['Country']
        return all_days


def validate_response_from_api(response):
    if 'message' in response.json():
        if response.json()['message'] == 'Not Found':
            raise ProcessorError.CountryInvalid
