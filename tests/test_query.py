import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.services import nl_service, query_service, dashboard_service

client = TestClient(app)

async def dummy_translate(req):
    return {
        "query": "SELECT 1 as x",
        "suggested_follow_up_questions": ["next"]
    }

async def dummy_execute(sql):
    return {
        "success": True,
        "data": [{"x": 1}],
        "metadata": {"row_count": 1, "columns": ["x"], "execution_time_ms": 1},
    }

class DummyDashboard:
    async def generate_suggestions(self, data, question):
        return {"suggestions": [{"type": "table", "title": "t"}]}

def test_orchestrator_flow(monkeypatch):
    monkeypatch.setattr(nl_service, "translate_question_to_query", dummy_translate)
    monkeypatch.setattr(query_service, "execute_query", dummy_execute)
    monkeypatch.setattr(dashboard_service, "DashboardService", lambda: DummyDashboard())

    resp = client.post("/", json={"question": "ping"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["sql"].lower().startswith("select")
    assert data["data"][0]["x"] == 1
