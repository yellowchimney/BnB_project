DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS spaces;
DROP SEQUENCE IF EXISTS spaces_id_seq;


CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phonenumber VARCHAR
);

CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR,
    price_per_night INTEGER,
    owner_id INTEGER
);


INSERT INTO users (username, email, password, phonenumber) VALUES ('Gromit', 'gromit@wallace.com', 'passw0rd1', '07867564876');
INSERT INTO users (username, email, password, phonenumber) VALUES ('Wallace', 'wallace@wallace.com', 'passw0rd2', '07867564123');

INSERT INTO spaces (name, description, price_per_night, owner_id) VALUES ('Flat', 'Lovely flat', 5, 2);
INSERT INTO spaces (name, description, price_per_night, owner_id) VALUES ('Kennel', 'The dog house', 1, 1);