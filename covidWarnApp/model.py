import hashlib
import os

from flask import current_app
from covidWarnApp.database import db


class Users(db.Model):
    # __tablename__= 'users'

    id_user = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User: {self.alias}"
