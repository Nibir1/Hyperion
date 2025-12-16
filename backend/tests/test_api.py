"""
Integration Tests for API Routes
--------------------------------
Tests health checks, calculation endpoints, and mocks the AI service.
"""
from unittest.mock import patch
from app.main import app

def test_health_check(client):
    """
    Verify system health endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "pandas" in data["modules"]

def test_calculate_endpoint(client):
    """
    Verify the calculation endpoint accepts JSON and returns valid data.
    """
    payload = {
        "num_engines": 4,
        "solar_mw": 50,
        "battery_mwh": 10
    }
    
    response = client.post("/api/calculate", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Check structure matches Pydantic schema
    assert "kpis" in data
    assert "charts" in data
    assert len(data["charts"]) == 24
    assert data["kpis"]["total_capex_usd"] > 0

@patch("app.ai_service.generate_proposal_text")
def test_ai_proposal_mock(mock_ai, client):
    """
    Test the AI endpoint WITHOUT calling OpenAI.
    We mock the internal function to return a static string.
    """
    # Define what the mock should return
    mock_ai.return_value = "This is a mocked AI proposal for testing."
    
    payload = {
        "num_engines": 4,
        "solar_mw": 50,
        "battery_mwh": 10
    }
    
    response = client.post("/api/generate-proposal", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["proposal_text"] == "This is a mocked AI proposal for testing."
    
    # Verify our mock was actually called once
    mock_ai.assert_called_once()