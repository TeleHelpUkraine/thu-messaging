def test_webhook_receives_json(client):
    response = client.post('/webhook', json={"test": "data"})
    assert response.status_code == 200
    assert response.get_json() == {"status": "received"}
