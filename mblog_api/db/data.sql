CREATE TABLE IF NOT EXISTS users
(
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	login varchar(255) NOT NULL,
	secret varchar(255) NOT NULL,
	admin bool,
	CONSTRAINT users_pkey PRIMARY KEY (id),
	CONSTRAINT users_unq_login UNIQUE (login)
);
ALTER TABLE users OWNER TO mblog;

INSERT INTO users (login, secret, admin)
  VALUES ('zeus', '167b208b5899df2a16a8c0b1d19a4c24', true)
  ON CONFLICT DO NOTHING;

CREATE TABLE IF NOT EXISTS posts
(
  id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
  uid int4 NOT NULL,
  "date" timestamp NOT NULL,
  text varchar(255),
  CONSTRAINT posts_pkey PRIMARY KEY (id),
  CONSTRAINT posts_fk_uid FOREIGN KEY (uid) REFERENCES users (id)
    ON DELETE CASCADE ON UPDATE CASCADE
);
ALTER TABLE posts OWNER TO mblog;
CREATE INDEX IF NOT EXISTS posts_idx_uid ON posts USING btree(uid);
CREATE INDEX IF NOT EXISTS posts_idx_date ON posts USING btree("date");

CREATE TABLE IF NOT EXISTS tags
(
  tag varchar(30) NOT NULL,
  pid int4 NOT NULL,
  CONSTRAINT tags_pkey PRIMARY KEY (tag, pid),
  CONSTRAINT tags_fk_pid FOREIGN KEY (pid) REFERENCES posts (id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS incidents
(
  uid int4 NOT NULL,
  "date" timestamp NOT NULL,
  device_id varchar(255) NOT NULL,
  kind int4 NOT NULL,
  CONSTRAINT incidents_pkey PRIMARY KEY (uid, "date", device_id, kind),
  CONSTRAINT incidents_fk_uid FOREIGN KEY (uid) REFERENCES users (id)
    ON DELETE CASCADE ON UPDATE CASCADE
);