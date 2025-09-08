import pytest
from incontext.db import get_db, dict_factory

def test_new_tethered_list(app, client, auth):
    # Get requests
    # User must be logged in
    response = client.get("/lists/new-tethered")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login()
    response = client.get("/lists/new-tethered")
    assert response.status_code == 200
    # Page provides all master lists as options
    with app.app_context():
        master_list_ids = get_db().execute("SELECT id from master_lists")
        for master_list_id in master_list_ids:
            option =  f'<input type="hidden" name="master_list_id" value="{master_list_id["id"]}">'
            assert option.encode() in response.data
    # Post requests
    # User must be logged in
    auth.logout()
    response = client.post("/lists/new-tethered")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
# Master list id must exist
    auth.login()
    data = dict(name="tethered", master_list_id = 3) 
    response = client.post("/lists/new-tethered", data=data)
    assert response.status_code == 404
    # A new record is added to `lists` and `list_tethers`.
    with app.app_context():
        db = get_db()
        db.row_factory = dict_factory
        lists_before = db.execute("SELECT id FROM lists").fetchall()
        list_tethers_before = db.execute("SELECT id FROM list_tethers").fetchall()
        data = dict(name="tethered", description="", master_list_id=1)
        response = client.post("/lists/new-tethered", data=data)
        lists_after = db.execute("SELECT id FROM lists").fetchall()
        list_tethers_after = db.execute("SELECT id FROM list_tethers").fetchall()
        assert len(lists_after) == len(lists_before) + 1
        assert len(list_tethers_after) == len(list_tethers_before) + 1
        # Redirected to the lists's view view
        assert response.status_code == 302
        assert response.headers["Location"] == "/lists/6/view"


def test_view_tethered_list(app, client, auth):
    response = client.get("/lists/5/view")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login("other", "other")
    response = client.get("/lists/5/view")
    assert response.status_code == 403


def test_new_untethered_content(app, client, auth):
    # Get requests
    response = client.get("/lists/5/items/new")
