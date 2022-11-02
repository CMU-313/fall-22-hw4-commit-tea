from flask import Flask
import pytest

from app.handlers.routes import configure_routes

attr_dict = {"Medu": 0, "Fedu": 3, "Mjob": "health", "Fjob": "teacher", "reason": "reputation",
			"studytime": 3, "failures": 1, "schoolsup": "yes", "famsup": "no",
			"paid": "yes", "higher": "yes", "internet": "yes", "health": 5, "absences": 16}
 
valid_attrs_1 = {"Medu":3, "Fedu": 2, "Mjob":"teacher", "Fjob":"other", "reason":"reputation", "studytime": 4, "failures": 3,
				"schoolsup":"no", "famsup":"yes", "paid":"no", "higher": "yes", "internet":"no", "health": 3, "absences": 49}
 
valid_attrs_2 = {"Medu":4, "Fedu":1, "Mjob":"services", "Fjob":"at_home","reason":"home","studytime":"1",
				 "failures": 2,"schoolsup":"yes","famsup":"yes","paid":"no","higher": "no","internet":"no",
				 "health": 2,"absences": 93}

valid_attrs_3 = {"Medu":1,"Fedu":0,"Mjob":"at_home", "Fjob":"health", "reason":"other", "studytime": 2,"failures": 5,
				 "schoolsup":"no", "famsup":"no", "paid":"yes", "higher": "yes", "internet":"no", "health":4, "absences":0}

valid_attrs_4 = {"Medu":2, "Fedu":4, "Mjob":"other", "Fjob":"services", "reason":"course", "studytime": 1, "failures": 0,
				 "schoolsup":"no", "famsup":"yes", "paid":"no", "higher": "yes", "internet":"yes", "health":1, "absences": 11}

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

def helper_test_extra_var(client, attr_dict, new_var, val_to_add):
	attr_dict_new = dict(attr_dict)
	attr_dict_new[new_var] = val_to_add
	def f():
		response = client.get("\predict", params=attr_dict_new)
		assert response.status_code == 400
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
	 
#Tests that check for response when argument is missing
def test_Medu_missing(client): helper_test_missing_var(client, attr_dict, "Medu")
def test_Fedu_missing(client): helper_test_missing_var(client, attr_dict, "Fedu")
def test_Mjob_missing(client): helper_test_missing_var(client, attr_dict, "Mjob")
def test_Fjob_missing(client): helper_test_missing_var(client, attr_dict, "Fjob")
def test_reason_missing(client): helper_test_missing_var(client, attr_dict, "reason")
def test_studytime_missing(client): helper_test_missing_var(client, attr_dict, "studytime")
def test_failures_missing(client): helper_test_missing_var(client, attr_dict, "failures")
def test_schoolsup_missing(client): helper_test_missing_var(client, attr_dict, "schoolsup")
def test_famsup_missing(client): helper_test_missing_var(client, attr_dict, "famsup")
def test_paid_missing(client): helper_test_missing_var(client, attr_dict, "paid")
def test_higher_missing(client): helper_test_missing_var(client, attr_dict, "higher")
def test_internet_missing(client): helper_test_missing_var(client, attr_dict, "internet")
def test_health_missing(client): helper_test_missing_var(client, attr_dict, "health")
def test_absences_missing(client): helper_test_missing_var(client, attr_dict, "absences")

#Tests that check for response when a parameter is invalid (i.e. wrong type)
def test_Medu_invalid(client): helper_test_invalid_var(client, attr_dict, "Medu", "high school")
def test_Fedu_invalid(client): helper_test_invalid_var(client, attr_dict, "Fedu", "college")
def test_Mjob_invalid(client): helper_test_invalid_var(client, attr_dict, "Mjob", 0)
def test_Fjob_invalid(client): helper_test_invalid_var(client, attr_dict, "Fjob", 1)
def test_reason_invalid(client): helper_test_invalid_var(client, attr_dict, "reason", 25)
def test_studytime_invalid(client): helper_test_invalid_var(client, attr_dict, "studytime", "3 hours")
def test_failures_invalid(client): helper_test_invalid_var(client, attr_dict, "failures", "none")
def test_schoolsup_invalid(client): helper_test_range_var(client, attr_dict, "schoolsup", 100)
def test_famsup_invalid(client): helper_test_range_var(client, attr_dict, "famsup", 20)
def test_paid_invalid(client): helper_test_range_var(client, attr_dict, "paid", 2)
def test_higher_invalid(client): helper_test_range_var(client, attr_dict, "higher", 1)
def test_internet_invalid(client): helper_test_range_var(client, attr_dict, "internet", 43)
def test_health_invalid(client): helper_test_range_var(client, attr_dict, "health", "not_an_int")
def test_absences_invalid(client): helper_test_range_var(client, attr_dict, "absences", "not_an_int")


#Tests that check when when a parameter is out of bounds but is the correct type
def test_Medu_range(client): helper_test_range_var(client, attr_dict, "Medu", 5)
def test_Fedu_range(client): helper_test_range_var(client, attr_dict, "Fedu", -1)
def test_Mjob_range(client): helper_test_range_var(client, attr_dict, "Mjob", "professor")
def test_Fjob_range(client): helper_test_range_var(client, attr_dict, "Fjob", "doctor")
def test_reason_range(client): helper_test_range_var(client, attr_dict, "reason", "sports")
def test_studytime_range(client): helper_test_range_var(client, attr_dict, "studytime", 0)
def test_failures_range(client): helper_test_range_var(client, attr_dict, "failures", 0.5)
def test_schoolsup_range(client): helper_test_range_var(client, attr_dict, "schoolsup", "y")
def test_famsup_range(client): helper_test_range_var(client, attr_dict, "famsup", "n")
def test_paid_range(client): helper_test_range_var(client, attr_dict, "paid", "n")
def test_higher_range(client): helper_test_range_var(client, attr_dict, "higher", "y")
def test_internet_range(client): helper_test_range_var(client, attr_dict, "internet", "y")
def test_health_range(client): helper_test_range_var(client, attr_dict, "health", 0)
def test_absences_range(client): helper_test_range_var(client, attr_dict, "absences", 94)

#Tests for extra variables in json input
def test_extra_medu(client) : helper_test_extra_var(client, attr_dict, "medu", 4)
def test_extra_random(client) : helper_test_extra_var(client, attr_dict, "extra", 4)
def test_extra_health(client) : helper_test_extra_var(client, attr_dict, "HEALTH", 4)