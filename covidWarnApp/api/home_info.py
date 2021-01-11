from random import choice
from experta import *
import requests
from flask import Blueprint
from flask import jsonify, render_template
from flasgger.utils import swag_from

from covidWarnApp.api.processor import Processor

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


@bp_homeinfo.route("/rule-checker/<string:country>", methods=['GET'])
@swag_from(methods=['GET'])
def rule(country):
    """
    Rule Checker
    ---
    tags:
      - RETE
    parameters:
      - in: path
        name: country
        type: string
        required: true
    responses:
      200:
        description: Status
    """

    # TODO Make a class, ans instantiate. Then rules modify his state.

    processor = Processor(country)

    processor.process()

    print("processor.active_cases")
    print(processor.active_cases)
    print("processor.means_list_slope")
    print(processor.means_list)
    print(processor.means_list_slope)

    engine1 = RobotCrossStreet()
    engine1.reset()
    engine1.declare(Data(means_list_slope=processor.means_list_slope))
    engine1.declare(Data(fatality_rate_range=processor.fatality_rate_range))
    engine1.declare(Data(fatality_rate_slope=processor.fatality_rate_slope))
    engine1.declare(Data(active_cases_slope=processor.active_cases_slope))
    engine1.run()
    print(engine1.alert_color)
    print("engine1.alert_color")

    return jsonify({"Color": engine1.alert_color, "Message": engine1.alert_message}), 200


class Data(Fact):
    """Info about the traffic light."""
    pass


class RobotCrossStreet(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.alert_color = "Green"
        self.alert_message = "It is safe to travel"

    @Rule(Data(fatality_rate_range='above'))
    def undertesting(self):
        self.alert_color = "Yellow"
        self.alert_message = "There could be more cases as a result of undertesting and exceeding the fatality range"

    @Rule(Data(color='red'))
    def red_light(self):
        print("Don't walk")

    @Rule(AS.light << Data(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light["color"])
