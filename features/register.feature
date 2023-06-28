Feature: Register API

    Scenario: Successful registration
        Given I have the register endpoint
        When I make a POST request with a valid payload
        Then I should register user successfully
    
    Scenario: Failed Registration
        Given I have the register endpoint
        When I make a POST request with invalid credentials
        Then I should receive a failed response