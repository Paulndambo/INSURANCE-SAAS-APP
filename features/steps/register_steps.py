import requests
from behave import given, when, then

@given("I have the register endpoint")
def step_impl(context):
    context.url = "http://127.0.0.1:8000/users/register/"


@when("I make a POST request with a valid payload")
def step_impl(context):
    payload = {
        "username": "daboski1",
        "password": "Paul@40781998",
        "email": "daboski12@gmail.com"
    }
    context.response = requests.post(context.url, json=payload)


@then('I should register user successfully')
def step_imp(context):
    assert context.response.status_code == 201,  "Expected a successful response"
