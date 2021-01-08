from flask import current_app
from flask import request
from flask import Blueprint
from flask import jsonify
from flasgger.utils import swag_from
from covidWarnApp import database
from covidWarnApp.api import COVID_API
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

    if 'number_days_window_delta' in put_data:
        # change first name
        params.number_days_window_delta = put_data['number_days_window_delta']

    try:
        # commit to persist into the database
        database.db.session.commit()
    except:
        current_app.logger.error("Error when attempting to modify rule with " + str(put_data) + " in the database.")
        return jsonify({'Error': "Something happened when attempting to modify rule in the Database"}), 400

    current_app.logger.info("Modification for rule with " + str(put_data) + " succeeded.")
    return jsonify({'rule': params.id, 'modify': 'OK'}), 200
