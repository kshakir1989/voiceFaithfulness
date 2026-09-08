import pytest
from fastapi.testclient import TestClient

from app.domain.store import store
from app.main import create_app
from app.providers.mocks import MockJudge, MockSTT, MockSummarizer


@pytest.fixture(autouse=True)
def _reset_store():
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client():
    return TestClient(create_app())


@pytest.fixture
def mock_providers():
    """CI-safe provider doubles (no Groq network)."""
    return {
        "stt": MockSTT(),
        "summarizer": MockSummarizer(),
        "judge": MockJudge(),
    }
