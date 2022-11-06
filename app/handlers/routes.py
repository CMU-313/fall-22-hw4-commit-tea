import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code

def check_missing(var):
    if not var:
        raise InvalidAPIUsage("Parameter missing!", 400)

def invalid_type(var):
    
    raise InvalidAPIUsage("Invalid type", 406)

def out_of_range(var):
    
    raise InvalidAPIUsage("Variable out of range", 422)
def validate(vars):
    for var in vars:
        check_missing(var)
        invalid_type(var)
        out_of_range(var)

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"

    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        Medu, Fedu, Mjob, Fjob, reason, studytime, failures, Schoolsup, Famsup, Paid, Higher, Internet, health, absences
        Medu = request.args.get('Medu')
        Fedu = request.args.get('Fedu')
        Mjob = request.args.get('Mjob')
        Fjob = request.args.get('Fjob')
        reason = request.args.get('reason'),
        studytime = request.args.get('studytime'),
        failures = request.args.get('failures')
        Schoolsup = request.args.get('Schoolsup')
        Famsup = request.args.get('Famsup'),
        Paid = request.args.get('Paid')
        Higher = request.args.get('Higher')
        Internet = request.args.get('Internet'),
        health = request.args.get('health'),
        absences = request.args.get('absences'),
        data = [[age], [health], [absences]]
        validate(data)
        if (length(request.args) > EXPECTED):
            raise  invalid_api_usage('Additional variables', 422)
        # age = request.args.get('age')
        # absences = request.args.get('absences')
        # health = request.args.get('health')
        # data = [[age], [health], [absences]]
        # query_df = pd.DataFrame({
        #     'age': pd.Series(age),
        #     'health': pd.Series(health),
        #     'absences': pd.Series(absences)
        # })
        # query = pd.get_dummies(query_df)
        # prediction = clf.predict(query)
        # return jsonify(np.ndarray.item(prediction))
