DROP TABLE IF EXISTS configuration;
DROP TABLE IF EXISTS assignment;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS window;
DROP TABLE IF EXISTS room;

CREATE TABLE configuration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    co2 INTEGER,
    humidity REAL,
    automatik_enable INTEGER NOT NULL
);

CREATE TABLE room (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    is_open INTEGER NOT NULL,
    automatik_enable INTEGER NOT NULL
);

CREATE TABLE window (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    is_open INTEGER NOT NULL,
    automatik_enable NOT NULL,
    FOREIGN KEY (room_id) REFERENCES room (id)
);

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin INTEGER NOT NULL
);

CREATE TABLE assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alias TEXT,
    user_id INTEGER NOT NULL,
    allowed INTEGER NOT NULL,
    room_id INTEGER,
    window_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (room_id) REFERENCES room (id),
    FOREIGN KEY (window_id) REFERENCES window (id)
);