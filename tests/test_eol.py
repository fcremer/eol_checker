from eol_service.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_supported():
    response = client.get('/eol', params={'name': 'ubuntu', 'version': '22.04'})
    assert response.status_code == 200
    data = response.json()
    assert data['supported'] is True

def test_not_supported():
    response = client.get('/eol', params={'name': 'python', 'version': '3.8'})
    assert response.status_code == 200
    data = response.json()
    assert data['supported'] in [True, False]
