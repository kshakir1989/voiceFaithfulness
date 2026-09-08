from app.domain.pipeline import (
    STAGE_ORDER,
    StageName,
    StageStatus,
    advance,
    can_start_run,
    initial_stages,
)


def test_initial_stages_pending():
    stages = initial_stages()
    assert len(stages) == len(STAGE_ORDER)
    assert all(v == StageStatus.PENDING.value for v in stages.values())


def test_advance_stage():
    stages = initial_stages()
    stages = advance(stages, StageName.TRANSCRIPT, StageStatus.RUNNING)
    assert stages["transcript"] == "running"


def test_can_start_requires_both_agents():
    assert can_start_run(transcription_agent_id="a", judge_agent_id="b") is True
    assert can_start_run(transcription_agent_id="", judge_agent_id="b") is False
    assert can_start_run(transcription_agent_id="a", judge_agent_id=None) is False
