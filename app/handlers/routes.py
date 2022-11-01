import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        """Home page for the application
    ---
    responses:
      200:
        description: Successful response
    """
        return "try the predict route it is great!"

    @app.route('/predict')
    def predict():
        """Route to predict a student's success based on some factors
    ---
    parameters:
      - in: query
        name: studytime
        type: int
        description: "Weekly study time (numeric: 1 - <2 hours, 2 - 2 to 5 hours, 3 - 5 to 10 hours, or 4 - >10 hours)"
        enum: ['1', '2', '3', '4']
        required: true
        default: '1'
      - in: query
        name: reason
        type: string
        description: "reason to choose this school (nominal: close to 'home', school 'reputation', 'course' preference or 'other')"
        enum: ['home', 'reputation', 'course', 'other']
        required: true
        default: '1'
      - in: query
        name: Fjob
        type: string
        description: "Father's job (nominal: 'teacher', 'health' care related, civil 'services' (e.g. administrative or police), 'at_home' or 'other'))"
        enum: ['teacher', 'health care', 'civil_services', 'at_home', 'other']
        required: true
        default: 'teacher'
      - in: query
        name: Mjob
        type: string
        description: "Mother's job (nominal: 'teacher', 'health' care related, civil 'services' (e.g. administrative or police), 'at_home' or 'other'))"
        enum: ['teacher', 'health care', 'civil_services', 'at_home', 'other']
        required: true
        default: 'teacher'
      - in: query
        name: Fedu
        type: int
        description: "Father's education (numeric: 0 - none, 1 - primary education (4th grade), 2 - 5th to 9th grade, 3 - secondary education or 4 - higher education)"
        enum: ['0', '1', '2', '3', '4']
        required: true
        default: '0'
      - in: query
        name: Medu
        type: int
        description: "Mother's education (numeric: 0 - none, 1 - primary education (4th grade), 2 - 5th to 9th grade, 3 - secondary education or 4 - higher education)"
        enum: ['0', '1', '2', '3', '4']
        required: true
        default: '0'
      - in: query
        name: absences
        type: int
        description: 'Number of school absences (numeric: from 0 to 93)'
        required: true
        default: '0'
      - in: query
        name: health
        type: int
        description: 'Current health status (numeric: from 1 - very bad to 5 - very good)'
        enum: ['1', '2', '3', '4', '5']
        required: true
        default: '1'
      - in: query
        name: internet
        type: int
        description: 'Internet access at home (binary: yes or no)'
        enum: ['0', '1']
        required: true
        default: '0'
      - in: query
        name: higher
        type: int
        description: 'Wants to take higher education (binary: yes or no)'
        enum: ['0', '1']
        required: true
        default: '0'
      - in: query
        name: paid
        type: int
        description: 'Extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)'
        enum: ['0', '1']
        required: true
        default: '0'
      - in: query
        name: paid
        type: int
        description: 'Extra paid classes within the course subject (Math or Portuguese) (binary: yes or no)'
        enum: ['0', '1']
        required: true
        default: '0'
      - in: query
        name: famsup
        type: int
        description: 'Family educational support (binary: yes or no)'
        enum: ['0', '1']
        required: true
        default: '0'
      - in: query
        name: schoolsup
        type: int
        description: 'Extra educational support (binary: yes or no)'
        enum: ['0', '1']
        required: true
        default: '0'
        
    responses:
      200:
        description: Successful response
      400:
        description: Missing parameters
      406:
        description: Invalid type
      422:
        description: Out of range
    """

        #use entries from the query string here but could also use json
        age = request.args.get('age')
        absences = request.args.get('absences')
        health = request.args.get('health')
        data = [[age], [health], [absences]]
        query_df = pd.DataFrame({
            'age': pd.Series(age),
            'health': pd.Series(health),
            'absences': pd.Series(absences)
        })
        query = pd.get_dummies(query_df)
        prediction = clf.predict(query)
        return jsonify(np.ndarray.item(prediction))
