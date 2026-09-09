Feature: Faithfulness dashboard shell

  Scenario: Placeholder spa loads
    Given the app is open
    Then I see the voiceFaithfulness brand

  Scenario: Teaching region shows ingest on load
    Given the app is open
    Then the teaching region shows the ingest concept

  Scenario: Successful run covers all five teaching concepts
    Given the app is open
    When I run the faithfulness pipeline
    Then the teaching log includes ingest transcript summary judge and aggregate

  Scenario: Empty dashboard shows no scores yet
    Given the app is open with a fresh store
    Then overall shows No scores yet
    And the graph region shows an empty state

  Scenario: Switch graph views after scores exist
    Given the app is open
    When I run the faithfulness pipeline
    Then I can select per-recording and overall graph views
