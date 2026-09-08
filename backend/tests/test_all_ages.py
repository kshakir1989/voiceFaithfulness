from app.policy.all_ages import is_all_ages_eligible, validate_audio_meta


def test_all_ages_ok():
    assert is_all_ages_eligible(title="Nature walk", transcript="Birds and trees.") is True


def test_all_ages_blocked():
    assert is_all_ages_eligible(transcript="Contains adult content here") is False


def test_empty_audio_rejected():
    ok, msg = validate_audio_meta(size_bytes=0, content_type="audio/mpeg")
    assert ok is False
    assert msg
