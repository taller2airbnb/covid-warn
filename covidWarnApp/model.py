import hashlib
import os

from flask import current_app
from covidWarnApp.database import db

DEFAULT_NUMBER_DAYS_WINDOW_DELTA = 7


class RulesParams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_days_window_delta = db.Column(db.Integer, nullable=False, default=DEFAULT_NUMBER_DAYS_WINDOW_DELTA)

    def __repr__(self):
        return f"Nation: {self.alias}"


def insert_initial_values():
    db.session.add(RulesParams(id=0, number_days_window_delta=DEFAULT_NUMBER_DAYS_WINDOW_DELTA))
    db.session.commit()