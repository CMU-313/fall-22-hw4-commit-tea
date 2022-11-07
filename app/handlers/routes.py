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



def configure_routes(app):
    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)
    
    @app.errorhandler(InvalidAPIUsage)
    def invalid_api_usage(e):       
        return jsonify(e.to_dict()), e.status_code

    @app.route('/')
    def hello():
        return "try the predict route it is great!"
    
    def check_missing(param, passed_args):
        if param not in passed_args:
            raise InvalidAPIUsage("Parameter missing!", 400)
        
    def invalid_type(param, var):
        if (param == "age"):
            if (not var.isnumeric()):
                raise InvalidAPIUsage("Invalid type!", 406)
        elif (param == "reason"):
            if (not var.isalpha()):
                    raise InvalidAPIUsage("Invalid type!", 406)  
        elif (param == "studytime"):
            if (not var.isnumeric()):
                    raise InvalidAPIUsage("Invalid type!", 406)
        elif (param == "famsup"):
            if (not var.isalpha()):
                raise InvalidAPIUsage("Invalid type!", 406)
        elif (param == "internet"):
            if (not var.isalpha()):
                raise InvalidAPIUsage("Invalid type!", 406)
        elif (param == "health"):
            if (not var.isnumeric()):
                raise InvalidAPIUsage("Invalid type!", 406)  
        elif (param == "absences"):
            if (not var.isnumeric()):
                raise InvalidAPIUsage("Invalid type!", 406)
                

    def out_of_range(param, var):
        if (param == "age"):
            if (int(var) < 15 or int(var) > 22):
                raise InvalidAPIUsage("Out of range!", 422)
        elif (param == "reason"):
            options = ['home', 'reputation', 'course', 'other']
            if (var not in options):
                raise InvalidAPIUsage("Out of range!", 422)
        elif (param == "studytime"):
            if (int(var) < 1 or int(var) > 4):
                raise InvalidAPIUsage("Out of range!", 422)
        elif (param == "famsup"):
            if (var != "yes" and var != "no"):
                raise InvalidAPIUsage("Out of range!", 422)
        elif (param == "internet"):
            if (var != "yes" and var != "no"):
                raise InvalidAPIUsage("Out of range!", 422)
        elif (param == "health"):
            if (int(health) < 1 or int(health) > 5):
                raise InvalidAPIUsage("Out of range!", 422)
        elif (param == "absences"):
            if (int(var) < 0 or int(var) > 93):
                raise InvalidAPIUsage("Out of range!", 422)
            
    def validate(params, passed_args):
        for i in range(len(params)):
            check_missing(params[i], passed_args)
        for i in range(len(params)):
            invalid_type(params[i], passed_args[params[i]][0])
        for i in range(len(params)):
            out_of_range(params[i], passed_args[params[i]][0])        

    def quantifyreason(reason):
        if reason == 'home':
            return 1
        elif reason == 'reputation':
            return 2
        elif reason == 'course':
            return 3
        elif reason == 'other':
            return 0
    
    def fix_values(df):
        df['famsup'] = np.where(df['famsup']=='yes', 1, 0)
        df['internet'] = np.where(df['internet']=='yes', 1, 0)
        df['reason'] = df['reason'].apply(quantifyreason)

    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        age = request.args.get('age')
        reason = request.args.get('reason'),
        studytime = request.args.get('studytime'),
        famsup = request.args.get('famsup'),
        internet = request.args.get('internet'),
        health = request.args.get('health'),
        absences = request.args.get('absences'),
        data = [[age], [reason], [studytime], [famsup], [internet], [health], [absences]]
        param_names = ['age', 'reason', 'studytime', 'famsup', 'internet', 'health', 'absences']
        passed_args = request.args.to_dict(flat=False)
        if (len(request.args) > len(param_names)):
            raise InvalidAPIUsage("Extra parameters!", 422)
        validate(param_names, passed_args)
        
        query_df = pd.DataFrame({
            'age': pd.Series(age),
            'reason': pd.Series(reason),
            'studytime': pd.Series(studytime),
            'famsup': pd.Series(famsup),
            'internet': pd.Series(famsup),
            'health': pd.Series(health),
            'absences': pd.Series(absences)
        })
        fix_values(query_df)
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.ndarray.item(prediction))