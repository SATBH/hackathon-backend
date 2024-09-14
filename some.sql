create table users (id TEXT PRIMARY KEY, name TEXT, email TEXT);


create table measurements (
  timestamp datetime default current_timestamp,
  temperature real,
  heartrate real,
  respiratory_frequency real,
  user_id INTEGER,
  movement real,
  snores real,
  PRIMARY KEY (timestamp, user_id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);
