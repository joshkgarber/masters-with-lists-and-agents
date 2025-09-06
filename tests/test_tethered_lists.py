import pytest
from incontext.db import get_db, dict_factory

def test_create(app, client, auth):
    # User must be logged in
    response = client.get("/lists/new-tethered")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login()
    response = client.get("/lists/new-tethered")
    assert response.status_code == 200
