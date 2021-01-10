import hashlib
import os

from flask import current_app
from covidWarnApp.database import db

DEFAULT_NUMBER_DAYS_WINDOW_DELTA = 7
DEFAULT_JUMP_DAYS = 14
DEFAULT_TOTAL_JUMPS = 3
DEFAULT_FATALITY_RATE = 2.7
DEFAULT_FATALITY_RATE_VARIATION = 0.1


class RulesParams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_days_window_delta = db.Column(db.Integer, nullable=False, default=DEFAULT_NUMBER_DAYS_WINDOW_DELTA)
    jump_days = db.Column(db.Integer, nullable=False, default=DEFAULT_JUMP_DAYS)
    total_jumps = db.Column(db.Integer, nullable=False, default=DEFAULT_TOTAL_JUMPS)
    fatality_rate = db.Column(db.Float, nullable=False, default=DEFAULT_FATALITY_RATE)
    fatality_rate_variation = db.Column(db.Float, nullable=False, default=DEFAULT_FATALITY_RATE_VARIATION)

    def __repr__(self):
        return f"Nation: {self.id}"


def insert_initial_values():
    db.session.add(RulesParams(id=0, number_days_window_delta=DEFAULT_NUMBER_DAYS_WINDOW_DELTA,
                               jump_days=DEFAULT_JUMP_DAYS, total_jumps=DEFAULT_TOTAL_JUMPS,
                               fatality_rate=DEFAULT_FATALITY_RATE,
                               fatality_rate_variation=DEFAULT_FATALITY_RATE_VARIATION))
    db.session.commit()
