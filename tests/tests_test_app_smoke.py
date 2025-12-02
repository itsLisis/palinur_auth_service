def test_openapi_available(client):
    """
    Basic smoke test to ensure the app starts and OpenAPI is served.
    Keeps the test resilient if you hide docs in prod (adjust as needed).
    """
    r = client.get("/openapi.json")
    assert r.status_code == 200
    data = r.json()
    assert "paths" in data