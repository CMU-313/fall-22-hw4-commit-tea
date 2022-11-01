from flask import Flask
import pytest

from app.handlers.routes import configure_routes

attr_dict = {"Medu": 3, "Fedu": 2, "Mjob": "health", "Fjob": "teacher", "reason": "reputation", 
             "studytime": 3, "failures": 2, "schoolsup": "yes", "famsup": "no", 
             "paid": "yes", "higher": "yes", "internet": "yes", "health": 2, "absences": 16}

@pytest.fixture()
def client():
    app = Flask(__name__)
    return app.test_client()

    
def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'
 
def helper_test_missing_var(client, attr_dict, var):
    attr_dict_new = dict(attr_dict)
    del attr_dict_new[var]
    def f():
        response = client.get("\predict", params=attr_dict_new)
        assert response.status_code == 400
    return f
 
def helper_test_invalid_var(client, attr_dict, var, new_val):
    attr_dict_new = dict(attr_dict)
    attr_dict_new[var] = new_val
    def f():
        response = client.get("\predict", params=attr_dict_new)
        assert response.status_code == 406
    return f

def helper_test_range_var(client, attr_dict, var, new_val):
    attr_dict_new = dict(attr_dict)
    attr_dict_new[var] = new_val
    def f():
        response = client.get("\predict", params=attr_dict_new)
        assert response.status_code == 422
    return f
 
def helper_test_valid(client, attr_dict):
    attr_dict_new = dict(attr_dict)
    response = client.get("\predict", params=attr_dict_new)
    assert response.status_code == 200

def test_all_valid(client, attr_dict_list):
	for attr_dict in attr_dict_list:
		helper_test_valid(client, attr_dict)  
     

def test_Medu_missing(client): helper_test_missing_var(client, attr_dict, "Medu")
def test_Fedu_missing(client): helper_test_missing_var(client, attr_dict, "Fedu")
def test_Mjob_missing(client): helper_test_missing_var(client, attr_dict, "Mjob")
def test_Fjob_missing(client): helper_test_missing_var(client, attr_dict, "Fjob")
def test_reason_missing(client): helper_test_missing_var(client, attr_dict, "reason")
def test_studytime_missing(client): helper_test_missing_var(client, attr_dict, "studytime")
def test_failures_missing(client): helper_test_missing_var(client, attr_dict, "failures")

# how to test other than string or int?
def test_Medu_invalid(client): helper_test_invalid_var(client, attr_dict, "Medu", "high school")
def test_Fedu_invalid(client): helper_test_invalid_var(client, attr_dict, "Fedu", "college")
def test_Mjob_invalid(client): helper_test_invalid_var(client, attr_dict, "Mjob", 0)
def test_Fjob_invalid(client): helper_test_invalid_var(client, attr_dict, "Fjob", 1)
def test_reason_invalid(client): helper_test_invalid_var(client, attr_dict, "reason", 25)
def test_studytime_invalid(client): helper_test_invalid_var(client, attr_dict, "studytime", "3 hours")
def test_failures_invalid(client): helper_test_invalid_var(client, attr_dict, "failures", "none")

def test_Medu_range(client): helper_test_range_var(client, attr_dict, "Medu", 5)
def test_Fedu_range(client): helper_test_range_var(client, attr_dict, "Fedu", -1)
def test_Mjob_range(client): helper_test_range_var(client, attr_dict, "Mjob", "professor")
def test_Fjob_range(client): helper_test_range_var(client, attr_dict, "Fjob", "doctor")
def test_reason_range(client): helper_test_range_var(client, attr_dict, "reason", "sports")
def test_studytime_range(client): helper_test_range_var(client, attr_dict, "studytime", 0)
def test_failures_range(client): helper_test_range_var(client, attr_dict, "failures", 0.5)
