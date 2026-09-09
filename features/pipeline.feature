Feature: Faithfulness pipeline

  Scenario: Score a preloaded recording end-to-end
    Given the app is open
    And recordings and agents are loaded
    When I run the faithfulness pipeline
    Then I see a completed score and overall percentage

  Scenario: Choose a non-default transcription agent
    Given the app is open
    And recordings and agents are loaded
    When I select a non-default transcription agent
    And I run the faithfulness pipeline
    Then the completed score shows that transcription agent

  Scenario: Choose a non-default judge agent
    Given the app is open
    And recordings and agents are loaded
    When I select a non-default judge agent
    And I run the faithfulness pipeline
    Then the completed score shows that judge agent

  Scenario: Preview a recording before running
    Given the app is open
    And recordings and agents are loaded
    Then I can listen to the selected recording in the audio preview

  Scenario: See transcript and summary after a run
    Given the app is open
    And recordings and agents are loaded
    When I run the faithfulness pipeline
    Then I see the transcript text
    And I see the summary text

  Scenario: Upload a local all-ages recording
    Given the app is open
    When I upload a valid all-ages audio file
    Then the recording appears in the picker

  Scenario: Rate limit shows an explicit message
    Given the app is open
    When the pipeline hits a free-tier rate limit
    Then I see a rate limit error banner
    And the overall percentage is unchanged

  Scenario: Second run blocked while one is in progress
    Given the app is open
    And another pipeline run is already active
    When I try to start another run
    Then I see a run-in-progress error
