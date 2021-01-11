from flask import current_app
from flask import request
from flask import Blueprint
from flask import jsonify
from flasgger.utils import swag_from
from covidWarnApp import database
from covidWarnApp.Errors.CovidWarnException import CovidWarnException
from covidWarnApp.api.utils import validate_number_days_window_delta, validate_number_jumps, validate_number_jump_days, \
    validate_fatality_rate_data
from covidWarnApp.model import RulesParams

bp_params = Blueprint('params', __name__, url_prefix='/params/')


@bp_params.route("/", methods=['PUT'])
@swag_from(methods=['PUT'])
def business():
    """
    CovidWarn Params Update
    To modify params for metrics and rules
    ---
    tags:
      - params
    consumes:
      - application/json
    parameters:
      - name: body
        in: body
        required: true
        schema:
            properties:
              number_days_window_delta:
                type: integer
                description: Number of days to calculate the delta of cases
              jump_days:
                type: integer
                description: cada cuantos dias sacas una foto (mirando pa atras)
              total_jumps:
                type: integer
                description: Number of jumps
              fatality_rate:
                type: number
                description: Number of fatality rate
              fatality_rate_variation:
                type: number
                description: variation of fatality rate
    responses:
      200:
        description: A successful user modification.
        schema:
          properties:
              id:
                type: integer
                description: Unique identifier representing the user.
              modify_user:
                type: string
                description: Validation, expected 'Ok'.
    """
    put_data = request.get_json()
    current_app.logger.info('Modifying params: ' + str(put_data))

    params = RulesParams.query.first()

    # TODO nuevos params to database

    try:
        if 'number_days_window_delta' in put_data:
            validate_number_days_window_delta(put_data["number_days_window_delta"])
            params.number_days_window_delta = put_data['number_days_window_delta']
        if 'jump_days' in put_data:
            validate_number_jump_days(put_data["jump_days"])
            params.jump_days = put_data['jump_days']
        if 'total_jumps' in put_data:
            validate_number_jumps(put_data["total_jumps"])
            params.total_jumps = put_data['total_jumps']
        if 'fatality_rate' in put_data:
            validate_fatality_rate_data(put_data["fatality_rate"])
            params.fatality_rate = put_data['fatality_rate']
        if 'fatality_rate_variation' in put_data:
            validate_fatality_rate_data(put_data["fatality_rate_variation"])
            params.fatality_rate_variation = put_data['fatality_rate_variation']

    except CovidWarnException as e:
        current_app.logger.error("Modification for rule with " + str(put_data) + " failed.")
        return jsonify({'Error': e.message}), e.error_code

    try:
        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Error when attempting to modify rule with " + str(put_data) + " in the database.")
        return jsonify({'Error': "Something happened when attempting to modify rule in the Database"}), 400

    current_app.logger.info("Modification for rule with " + str(put_data) + " succeeded.")
    return jsonify({'rule': params.id, 'modify': 'OK'}), 200
