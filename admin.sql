DROP TABLE IF EXISTS administrator;

CREATE TABLE administrator(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password varchar(255)
);