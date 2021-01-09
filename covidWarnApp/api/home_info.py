from scipy.stats import linregress
from random import choice
from experta import *
import requests
from flask import Blueprint
from flask import jsonify, render_template
from flasgger.utils import swag_from

from covidWarnApp.api.calc_process import process_means
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

    total_jumps = 3
    a = range(total_jumps)

    means_list, fatality_rate, active_cases = process_means(country, number_days_window_delta, 14, total_jumps)
    for result in [means_list, fatality_rate, active_cases]:
        print(result)
        print(linregress(a, result))
    print("...----...")

    engine1 = RobotCrossStreet()
    engine1.reset()
    engine1.declare(Light(color=choice(['green', 'yellow', 'blinking-yellow', 'red'])))
    engine1.run()

    return jsonify(means_list, fatality_rate, active_cases), 200


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
