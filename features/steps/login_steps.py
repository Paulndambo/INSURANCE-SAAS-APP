import requests
from behave import given, when, then


@given('I have the login endpoint')
def step_impl(context):
    context.url = 'http://127.0.0.1:8000/api/login/'


@when('I make a POST request with valid credentials')
def step_impl(context):
    payload = {
        'username': 'admin',
        'password': '1234'
    }
    context.response = requests.post(context.url, json=payload)


@then('I should receive a successful response')
def step_impl(context):
    assert context.response.status_code == 200, "Expected a successful response"


@when('I make a POST request with invalid credentials')
def step_impl(context):
    payload = {
        'username': 'invalidusername',
        'password': 'invalidpassword'
    }
    context.response = requests.post(context.url, json=payload)


@then('I should receive an error response')
def step_impl(context):
    assert context.response.status_code == 400, "Expected an error response"
