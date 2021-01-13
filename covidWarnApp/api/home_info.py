from covidWarnApp.Errors import ProcessorError
from random import choice
from experta import *
from flask import Blueprint, current_app
from flask import jsonify, render_template
from flasgger.utils import swag_from

from covidWarnApp.Errors import CovidWarnException
from covidWarnApp.api.processor import Processor

bp_homeinfo = Blueprint('status_info', __name__, url_prefix='/')


@bp_homeinfo.route("/", methods=['GET'])
@swag_from(methods=['GET'])
def home():
    return render_template("home.html")


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
    try:
        processor = Processor(country)

        processor.process()
    except CovidWarnException as e:
        current_app.logger.error("Error while processing " + str(country))
        return jsonify({'Error': e.message}), e.error_code

    print("processor.active_cases")
    print(processor.active_cases)
    print(processor.active_cases_slope)
    print("processor.means_list_slope")
    print(processor.means_list)
    print(processor.means_list_slope)
    print(processor.variation_means_list_slope)
    print("processor.fatality_rate_range")
    print(processor.fatality_rate)
    print(processor.fatality_rate_range)
    print(processor.fatality_rate_slope)

    engine1 = RobotCrossStreet()
    engine1.reset()
    engine1.declare(Data(means_list_slope=processor.means_list_slope))
    engine1.declare(Data(fatality_rate_range=processor.fatality_rate_range))
    engine1.declare(Data(fatality_rate_slope=processor.fatality_rate_slope))
    engine1.declare(Data(active_cases_slope=processor.active_cases_slope))
    engine1.declare(Data(variation_means_list_slope=processor.variation_means_list_slope))
    engine1.run()

    return jsonify({"Country": processor.country, "Color": engine1.alert_color, "Message": engine1.alert_message}), 200


class Data(Fact):
    """Info about the covid calcs."""
    pass


class RobotCrossStreet(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.alert_color = "Green"
        self.alert_message = "It is safe to travel"

    @Rule(AND(Data(means_list_slope='positive'),
              Data(variation_means_list_slope='tripling')))
    def red_increasing_cases(self):
        self.alert_color = "Red"
        self.alert_message = "We recommend not to travel since cases are increasing too quickly"

    @Rule(AND(Data(means_list_slope='positive'),
              Data(variation_means_list_slope='unstable')))
    def orange_increases(self):
        self.alert_color = "Orange"
        self.alert_message = "We suggest not to travel since cases are increasing"

    @Rule(AND(Data(fatality_rate_range='above'),
          Data(variation_means_list_slope='stable')))
    def undertesting(self):
        self.alert_color = "Yellow"
        self.alert_message = "There could be more cases as a result of undertesting and exceeding the fatality range"

    @Rule(AND(Data(means_list_slope='positive'), Data(active_cases_slope='positive'),
              Data(variation_means_list_slope='stable')))
    def stable_increasing(self):
        self.alert_color = "Yellow"
        self.alert_message = "Situation stable but cases in slight increment."
