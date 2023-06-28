Feature: Login API
    Scenario: Successful login
        Given I have the login endpoint
        When I make a POST request with valid credentials
        Then I should receive a successful response

    Scenario: Invalid credentials
        Given I have the login endpoint
        When I make a POST request with invalid credentials
        Then I should receive an error response



