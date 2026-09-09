"""US5: teaching messages catalog for Teach-in-UI."""

from app.domain.teaching import CONCEPT_ORDER, MESSAGES


def test_teaching_messages_lists_five_concepts(client):
    r = client.get("/api/teaching/messages")
    assert r.status_code == 200
    body = r.json()
    concepts = [m["concept"] for m in body["messages"]]
    assert concepts == list(CONCEPT_ORDER)
    assert len(body["messages"]) == 5
    assert body["concepts"] == list(CONCEPT_ORDER)
    for msg in body["messages"]:
        assert msg["id"].startswith("teach-")
        assert msg["body"].strip()


def test_teaching_bodies_match_static_catalog(client):
    r = client.get("/api/teaching/messages").json()
    by_id = {m["id"]: m["body"] for m in r["messages"]}
    for msg in MESSAGES:
        assert by_id[msg["id"]] == msg["body"]
