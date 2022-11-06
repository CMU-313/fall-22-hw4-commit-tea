from flask import Flask
import pytest

from app.handlers.routes import configure_routes

attr_dict = {"age": 18,  "reason": "reputation", "studytime": 3, "famsup": "no", "internet": "yes", "health": 5, "absences": 16}
 
valid_attrs_1 = {"age":15, "reason":"reputation", "studytime": 4, "famsup":"yes", "internet":"no", "health": 3, "absences": 49}
 
valid_attrs_2 = {"age":17, "reason":"home","studytime":"1", "famsup":"yes", "internet":"no", "health": 2,"absences": 93}

valid_attrs_3 = {"age":19, "reason":"other", "studytime": 2, "famsup":"no", "internet":"no", "health":4, "absences":0}

valid_attrs_4 = {"age":22, "reason":"course", "studytime": 1, "famsup":"yes", "internet":"yes", "health":1, "absences": 11}

@pytest.fixture()
def client():
	app = Flask(__name__)
	return app.test_client()

@pytest.fixture()
def attr_dict_list():
	return [attr_dict, valid_attrs_1, valid_attrs_2, valid_attrs_3, valid_attrs_4]

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
    response = client.get("/predict", json=attr_dict_new)
    assert response.status_code == 400
 
def helper_test_invalid_var(client, attr_dict, var, new_val):
    attr_dict_new = dict(attr_dict)
    attr_dict_new[var] = new_val
    response = client.get("/predict", json=attr_dict_new)
    assert response.status_code == 406

def helper_test_range_var(client, attr_dict, var, new_val):
    attr_dict_new = dict(attr_dict)
    attr_dict_new[var] = new_val
    response = client.get("/predict", json=attr_dict_new)
    assert response.status_code == 422
 
def helper_test_valid(client, attr_dict):
    attr_dict_new = dict(attr_dict)
    response = client.get("/predict", json=attr_dict_new)
    assert response.status_code == 200

def test_all_valid(client, attr_dict_list):
	for d in attr_dict_list:
		helper_test_valid(client, d)  

def helper_test_extra_var(client, attr_dict, new_var, val_to_add):
    attr_dict_new = dict(attr_dict)
    attr_dict_new[new_var] = val_to_add
    response = client.get("\predict", json=attr_dict_new)
    assert response.status_code == 422

def helper_test_missing_and_invalid(client, attr_dict, var_to_delete, invalid_var, invalid_value):
    attr_dict_new = dict(attr_dict)
    del attr_dict_new[var_to_delete]
    attr_dict_new[invalid_var] = invalid_value
    response = client.get("\predict", json=attr_dict_new)
    assert response.status_code == 400
     
#Tests that check for response when argument is missing
def test_age_missing(client): helper_test_missing_var(client, attr_dict, "age")
def test_reason_missing(client): helper_test_missing_var(client, attr_dict, "reason")
def test_studytime_missing(client): helper_test_missing_var(client, attr_dict, "studytime")
def test_famsup_missing(client): helper_test_missing_var(client, attr_dict, "famsup")
def test_internet_missing(client): helper_test_missing_var(client, attr_dict, "internet")
def test_health_missing(client): helper_test_missing_var(client, attr_dict, "health")
def test_absences_missing(client): helper_test_missing_var(client, attr_dict, "absences")

#Tests that check for response when a parameter is invalid (i.e. wrong type)
def test_age_invalid(client): helper_test_invalid_var(client, attr_dict, "age", "not_an_age")
def test_reason_invalid(client): helper_test_invalid_var(client, attr_dict, "reason", 25)
def test_studytime_invalid(client): helper_test_invalid_var(client, attr_dict, "studytime", "3 hours")
def test_famsup_invalid(client): helper_test_range_var(client, attr_dict, "famsup", 20)
def test_internet_invalid(client): helper_test_range_var(client, attr_dict, "internet", 43)
def test_health_invalid(client): helper_test_range_var(client, attr_dict, "health", "not_an_int")
def test_absences_invalid(client): helper_test_range_var(client, attr_dict, "absences", "not_an_int")

#Tests that check when when a parameter is out of bounds but is the correct type
def test_age_range(client): helper_test_range_var(client, attr_dict, "age", 5)
def test_reason_range(client): helper_test_range_var(client, attr_dict, "reason", "sports")
def test_studytime_range(client): helper_test_range_var(client, attr_dict, "studytime", 0)
def test_famsup_range(client): helper_test_range_var(client, attr_dict, "famsup", "n")
def test_internet_range(client): helper_test_range_var(client, attr_dict, "internet", "y")
def test_health_range(client): helper_test_range_var(client, attr_dict, "health", 0)
def test_absences_range(client): helper_test_range_var(client, attr_dict, "absences", 94)

#Tests for extra variables in json input
def test_extra_age(client) : helper_test_extra_var(client, attr_dict, "age", 20)
def test_extra_random(client) : helper_test_extra_var(client, attr_dict, "extra", 4)
def test_extra_health(client) : helper_test_extra_var(client, attr_dict, "HEALTH", 4)

#Tests that missing variable error returned instead of invalid error when both are present
def test_missing_famsup_invalid_age(client): helper_test_missing_and_invalid(client, attr_dict, "famsup", "age", 1)
def test_missing_reason_invalid_internet(client): helper_test_missing_and_invalid(client, attr_dict, "reason", "internet", 43)