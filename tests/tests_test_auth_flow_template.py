def test_register_and_login_flow(client):
    """
    Template test showing a typical register -> login -> get /me flow.
    Update endpoints/fields to match your actual implementation.
    """
    # 1) Register
    register_payload = {"email": "alice@example.com", "password": "s3cret"}
    r = client.post("/auth/register", json=register_payload)
    # many apps return 201 on create, some 200 — adjust if needed
    assert r.status_code in (200, 201)
    body = r.json()

    # Optionally assert structure (adjust fields)
    assert "id" in body or "email" in body

    # 2) Login / token
    login_payload = {"username": "alice@example.com", "password": "s3cret"}
    r = client.post("/auth/token", data=login_payload)  # some implementations use form data
    assert r.status_code == 200
    token_resp = r.json()
    assert "access_token" in token_resp

    access_token = token_resp["access_token"]

    # 3) Authenticated endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    me = r.json()
    assert me.get("email") == "alice@example.com"