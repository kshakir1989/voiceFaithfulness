Feature: Live pipeline learning flow (002)
  As a learner
  I want trustworthy agent outputs and a clear flow UI
  So I can compare agents and understand faithfulness scores

  Scenario: Stub honesty is visible
    Given providers are stubbed
    When I open the dashboard
    Then I see a stub-mode warning

  Scenario: Transcription agent owns summary
    Given I select a transcription agent
    When the pipeline completes
    Then transcript and summary are attributed to that agent

  Scenario: Rationale is revealable
    Given a completed run with a score
    When I open Why this score
    Then I see the judge rationale or an honest empty state

  Scenario: Session history compares runs
    Given I completed two runs with different agents
    When I view session history
    Then I see both runs listed

  Scenario: Layout toggle
    Given the app is open
    When I switch Desktop and Mobile view
    Then the flow layout updates without losing controls

  Scenario: Demo reset
    Given session runs and scores exist
    When I clear demo data
    Then history and scores are empty and preloads remain
