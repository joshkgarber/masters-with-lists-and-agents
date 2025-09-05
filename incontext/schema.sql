DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS master_lists;
DROP TABLE IF EXISTS master_items;
DROP TABLE IF EXISTS master_details;
DROP TABLE IF EXISTS master_item_detail_relations;
DROP TABLE IF EXISTS master_list_item_relations;
DROP TABLE IF EXISTS master_list_detail_relations;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS details;
DROP TABLE IF EXISTS item_detail_relations;
DROP TABLE IF EXISTS lists;
DROP TABLE IF EXISTS list_item_relations;
DROP TABLE IF EXISTS list_detail_relations;
DROP TABLE IF EXISTS list_tethers;
DROP TABLE IF EXISTS untethered_content;
DROP TABLE IF EXISTS master_agents;
DROP TABLE IF EXISTS agents;
DROP TABLE IF EXISTS agent_models;
DROP TABLE IF EXISTS tethered_agents;


CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
    admin BOOL NOT NULL DEFAULT 0
);


CREATE TABLE master_lists (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	description TEXT,
	FOREIGN KEY (creator_id) REFERENCES users (id)
);


CREATE TABLE master_items (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	FOREIGN KEY (creator_id) REFERENCES users (id)
);


CREATE TABLE master_details (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	description TEXT,
	FOREIGN KEY (creator_id) REFERENCES users (id)
);


CREATE TABLE master_item_detail_relations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	master_item_id INTEGER NOT NULL,
	master_detail_id INTEGER NOT NULL,
	master_content TEXT,
	FOREIGN KEY (master_item_id) REFERENCES master_items (id)
	FOREIGN KEY (master_detail_id) REFERENCES master_details (id)
);


CREATE TABLE master_list_item_relations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	master_list_id INTEGER NOT NULL,
	master_item_id INTEGER NOT NULL,
	FOREIGN KEY (master_list_id) REFERENCES master_lists (id),
	FOREIGN KEY (master_item_id) REFERENCES master_items (id)
);


CREATE TABLE master_list_detail_relations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	master_list_id INTEGER NOT NULL,
	master_detail_id INTEGER NOT NULL,
	FOREIGN KEY (master_list_id) REFERENCES master_lists (id),
	FOREIGN KEY (master_detail_id) REFERENCES master_details (id)
);


CREATE TABLE list_tethers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    master_list_id INTEGER NOT NULL,
    FOREIGN KEY (list_id) REFERENCES lists (id),
    FOREIGN KEY (master_list_id) REFERENCES master_lists (id)
);


CREATE TABLE untethered_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    master_detail_id INTEGER NOT NULL,
    content TEXT,
    FOREIGN KEY (list_id) REFERENCES lists (id),
    FOREIGN KEY (item_id) REFERENCES items (id),
    FOREIGN KEY (master_detail_id) REFERENCES master_details (id)
);


CREATE TABLE items (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	FOREIGN KEY (creator_id) REFERENCES users (id)
);


CREATE TABLE details (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	description TEXT,
	FOREIGN KEY (creator_id) REFERENCES users (id)
);


CREATE TABLE item_detail_relations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	item_id INTEGER NOT NULL,
	detail_id INTEGER NOT NULL,
	content TEXT,
	FOREIGN KEY (item_id) REFERENCES items (id)
	FOREIGN KEY (detail_id) REFERENCES details (id)
);


CREATE TABLE lists (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	description TEXT,
    tethered BOOL NOT NULL DEFAULT 0,
	FOREIGN KEY (creator_id) REFERENCES users (id)
);


CREATE TABLE list_item_relations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	list_id INTEGER NOT NULL,
	item_id INTEGER NOT NULL,
	FOREIGN KEY (list_id) REFERENCES lists (id),
	FOREIGN KEY (item_id) REFERENCES items (id)
);


CREATE TABLE list_detail_relations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	list_id INTEGER NOT NULL,
	detail_id INTEGER NOT NULL,
	FOREIGN KEY (list_id) REFERENCES lists (id),
	FOREIGN KEY (detail_id) REFERENCES details (id)
);


CREATE TABLE master_agents (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	description TEXT NOT NULL,
	model_id INTEGER NOT NULL,
	role TEXT NOT NULL,
	instructions TEXT NOT NULL,
	FOREIGN KEY (creator_id) REFERENCES users (id),
	FOREIGN KEY (model_id) REFERENCES agent_models (id)
);


CREATE TABLE agents (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	name TEXT NOT NULL,
	description TEXT NOT NULL,
	model_id INTEGER NOT NULL,
	role TEXT NOT NULL,
	instructions TEXT NOT NULL,
	FOREIGN KEY (creator_id) REFERENCES users (id),
	FOREIGN KEY (model_id) REFERENCES agent_models (id)
);


CREATE TABLE agent_models (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	provider_name TEXT NOT NULL,
	provider_code TEXT NOT NULL,
	model_name TEXT NOT NULL,
	model_code TEXT NOT NULL,
	model_description TEXT NOT NULL
);


CREATE TABLE tethered_agents (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	creator_id INTEGER NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	master_agent_id INTEGER NOT NULL,
	FOREIGN KEY (master_agent_id) REFERENCES master_agents (id)
);

