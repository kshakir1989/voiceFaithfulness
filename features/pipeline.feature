Feature: Faithfulness pipeline US1
  Scenario: Score a preloaded recording end-to-end
    Given the app is open
    And recordings and agents are loaded
    When I run the faithfulness pipeline
    Then I see a completed score and overall percentage
