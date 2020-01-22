INSERT INTO room (is_open, automatic_enable, co2, humidity)
VALUES (1, 1, 720, 71.2);

INSERT INTO window (is_open, automatic_enable, room_id)
VALUES (1, 0, 1);

INSERT INTO window (is_open, automatic_enable, room_id)
VALUES (0, 0, 1);

INSERT INTO assignment (alias, allowed, user_id, room_id)
VALUES ("Wohnzimmer", 1, 1, 1);

INSERT INTO assignment (alias, allowed, user_id, window_id)
VALUES ("Schreibtisch", 1, 1, 1);

INSERT INTO assignment (alias, allowed, user_id, window_id)
VALUES ("Terasse", 1, 1, 2);