import datetime
from random import choice
from experta import *
import requests
from flask import Blueprint
from flask import jsonify, render_template
from flasgger.utils import swag_from

from covidWarnApp.api import COVID_API
from covidWarnApp.model import RulesParams

bp_homeinfo = Blueprint('status_info', __name__, url_prefix='/')


@bp_homeinfo.route("/", methods=['GET'])
@swag_from(methods=['GET'])
def home():
    return render_template("home.html")


@bp_homeinfo.route("/business-status")
@swag_from(methods=['GET'])
def business():
    """
    BusinessCore Health Check
    To Know if the BusinessCore Service is UP and running.
    ---
    tags:
      - health
    responses:
      200:
        description: Status
    """
    response = requests.get('https://taller2airbnb-businesscore.herokuapp.com/health')
    return response.json()


@bp_homeinfo.route("/health", methods=['GET'])
@swag_from(methods=['GET'])
def health():
    """
    Health Check
    To Know if the APP is UP and running.
    ---
    tags:
      - health
    responses:
      200:
        description: Status
    """

    return jsonify({"status": "UP", "from": "CovidWarn"}), 200


@bp_homeinfo.route("/rule-test/<string:country>", methods=['GET'])
@swag_from(methods=['GET'])
def rule(country):
    """
    Rule Check
    ---
    tags:
      - health
    parameters:
      - in: path
        name: country
        type: string
        required: true
    responses:
      200:
        description: Status
    """

    number_days_window_delta = RulesParams.query.first().number_days_window_delta
    my_list = populate_list(number_days_window_delta, country)

    engine1 = RobotCrossStreet()
    engine1.reset()
    engine1.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red'])))
    engine1.run()

    return jsonify(my_list), 200


def populate_list(number_days_window, country):
    populated_list = []
    all_days = requests.get(COVID_API + country)
    first = True
    for day in all_days.json():
        date_time_obj = datetime.datetime.strptime(day['Date'][:10], '%Y-%m-%d')
        if first:
            ordinal_first = date_time_obj.toordinal()
        n = date_time_obj.toordinal() - ordinal_first
        delta = 0
        fatality_rate = 0
        if n > number_days_window:
            delta = day['Confirmed'] - populated_list[n - number_days_window][1]
        first = False
        if day['Confirmed'] > 0:
            fatality_rate = day['Deaths'] / day['Confirmed']
        populated_list.append((n, day['Active'], day['Confirmed'], delta, fatality_rate, date_time_obj))
    return populated_list


class Light(Fact):
    """Info about the traffic light."""
    pass


class RobotCrossStreet(KnowledgeEngine):
    @Rule(Light(color='green'))
    def green_light(self):
        print("Walk")

    @Rule(Light(color='red'))
    def red_light(self):
        print("Don't walk")

    @Rule(AS.light << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light["color"])
