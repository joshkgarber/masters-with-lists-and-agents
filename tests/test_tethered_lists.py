import pytest
from incontext.db import get_db, dict_factory
from incontext.master_lists import get_master_list

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
        assert response.headers["Location"] == "/lists/8/view"


def test_view_tethered_list(app, client, auth):
    # User must be logged in and own the list
    response = client.get("/lists/5/view")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login("other", "other")
    response = client.get("/lists/5/view")
    assert response.status_code == 403
    auth.login()
    response = client.get("/lists/5/view")
    assert response.status_code == 200
    # Showing data of the master list
    with app.app_context():
        db = get_db()
        db.row_factory = dict_factory
        master_list_id = db.execute("SELECT master_list_id FROM list_tethers WHERE list_id = 5").fetchone()["master_list_id"]
        other_master_list_ids = db.execute("SELECT id FROM master_lists WHERE id != ?", (master_list_id,)).fetchall()
        master_list = get_master_list(master_list_id, False)
        assert master_list["name"].encode() in response.data
        assert master_list["description"].encode() in response.data
        master_items = master_list["master_items"]
        for master_item in master_items:
            assert master_item["name"].encode() in response.data
            for master_content in master_item["master_contents"]:
                assert master_content.encode() in response.data
        master_details = master_list["master_details"]
        for master_detail in master_details:
            assert master_detail["name"].encode() in response.data
        for other_master_list_id in other_master_list_ids:
            other_master_list = get_master_list(other_master_list_id["id"], False)
            assert other_master_list["name"].encode() not in response.data
            assert other_master_list["description"].encode() not in response.data
            other_master_items = db.execute("SELECT name FROM master_items WHERE id NOT IN (1, 2)")
            for other_master_item in other_master_items:
                assert other_master_item["name"].encode() not in response.data
                for master_content in master_item["master_contents"]:
                    assert master_content.encode() in response.data
            other_master_details = other_master_list["master_details"]
            for other_master_detail in other_master_details:
                assert other_master_detail["name"].encode() not in response.data
        untethered_contents = db.execute("SELECT item_id, content FROM untethered_content WHERE list_id = 5").fetchall()
        for ut in untethered_contents:
            assert ut["content"].encode() in response.data
            item_name = db.execute("SELECT name FROM items WHERE id = ?", (ut["item_id"],)).fetchone()
            assert item_name["name"].encode() in response.data
        other_untethered_contents = db.execute("SELECT item_id, content FROM untethered_content WHERE list_id != 5").fetchall()
        for out in other_untethered_contents:
            assert out["content"].encode() not in response.data
            item_name = db.execute("SELECT name FROM items WHERE id = ?", (out["item_id"],)).fetchone()
            assert item_name["name"].encode() not in response.data


def test_new_untethered_content(app, client, auth):
    # Get requests
    # You have to be logged in and own the list
    response = client.get("/lists/5/items/new")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login("other", "other")
    response = client.get("/lists/5/items/new")
    assert response.status_code == 403
    auth.login()
    response = client.get("/lists/5/items/new")
    assert response.status_code == 200
    with app.app_context():
        # The master list name and description are shown
        db = get_db()
        db.row_factory = dict_factory
        master_list_id = db.execute("SELECT master_list_id FROM list_tethers WHERE list_id = 5").fetchone()["master_list_id"]
        other_master_list_ids = db.execute("SELECT id FROM master_lists WHERE id != ?", (master_list_id,)).fetchall()
        master_list = get_master_list(master_list_id, False)
        assert master_list["name"].encode() in response.data
        assert master_list["description"].encode() in response.data
        # The master list details are shown
        master_details = master_list["master_details"]
        for master_detail in master_details:
            assert master_detail["name"].encode() in response.data
        # Master details from other master lists are not shown.
        for other_master_list_id in other_master_list_ids:
            other_master_list = get_master_list(other_master_list_id["id"], False)
            other_master_details = other_master_list["master_details"]
            for other_master_detail in other_master_details:
                assert other_master_detail["name"].encode() not in response.data
    # Post requests
    # You have to be logged in and own the list
    auth.logout()
    response = client.get("/lists/5/items/new")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"
    auth.login("other", "other")
    response = client.get("/lists/5/items/new")
    assert response.status_code == 403
    auth.login()
    response = client.get("/lists/5/items/new")
    assert response.status_code == 200
