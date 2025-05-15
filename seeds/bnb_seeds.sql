DROP TABLE IF EXISTS users CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP TABLE IF EXISTS spaces CASCADE;
DROP SEQUENCE IF EXISTS spaces_id_seq;
DROP TABLE IF EXISTS bookings CASCADE;
DROP SEQUENCE IF EXISTS bookings_id_seq;

CREATE SEQUENCE IF NOT EXISTS users_id_seq;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    phone_number VARCHAR
);

CREATE SEQUENCE IF NOT EXISTS spaces_id_seq;
CREATE TABLE spaces (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description VARCHAR,
    price_per_night INTEGER,
    owner_id INTEGER,
    url VARCHAR
);

CREATE SEQUENCE IF NOT EXISTS bookings_id_seq;
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ,
    space_id INTEGER REFERENCES spaces(id),
    date VARCHAR,
    is_approved BOOLEAN
);




INSERT INTO users (username, email, password, phone_number) VALUES ('Gromit', 'gromit@wallace.com', '$2b$12$odSf0B0I5gSqVFfddp92oeZudmdDj2gkNmlXT4do1S2roiT45N5tu', '07867564876');
INSERT INTO users (username, email, password, phone_number) VALUES ('Wallace', 'wallace@wallace.com', '$2b$12$ol40SdrozS89ixcXk8mFHOSHTiTpo9raSD7u4fX86CR5mg1W7u18G', '07867564123');
INSERT INTO users (username, email, password, phone_number)
VALUES ('Shawn', 'shawn@example.com', 'password_1', '123-456-7890');

INSERT INTO users (username, email, password, phone_number)
VALUES ('Bilbo', 'bilbo@shiremail.com', 'password_2', '111-222-3333');

INSERT INTO users (username, email, password, phone_number)
VALUES ('Sam', 'sam@hobbitmail.com', 'password_3', '444-555-6666');



INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('Bag End Bliss', 'A cozy burrow with a round green door, nestled into the side of a grassy hill in the Shire.', 80, 1, 'https://news.airbnb.com/wp-content/uploads/sites/4/2018/08/alt-3-underground-hygge.jpg');

INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('Mossy Hollow', 'A quaint hideaway with moss-covered walls and a fireplace that never goes out.', 65, 2, 'https://news.airbnb.com/wp-content/uploads/sites/4/2022/04/Second-Breakfast-Hideaway-1-Kootenay-Boundary-E-BC-1.jpeg');

INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('The Toadstool Den', 'This magical nook is surrounded by giant mushrooms and perfect for quiet reading.', 50, 3, 'https://www.bpmcdn.com/f/files/mission/import/2022-04/28932492_web1_220504-PWN-HobbitHouse_1.jpg;w=960;h=640;bgcolor=000000');

INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('Underhill Retreat', 'Tucked beneath the hills of Hobbiton, this peaceful retreat offers starlit garden views.', 75, 4, 'https://a0.muscache.com/im/pictures/2b6d8657-8daf-446b-81cf-413688ca0aae.jpg?im_w=720');

INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('Willowburrow', 'A sun-dappled home carved beneath an ancient willow tree, ideal for second breakfasts.', 70, 5, 'https://a0.muscache.com/im/pictures/1ce4f90a-c649-47b5-b5c9-9420cffd1c8f.jpg?im_w=720');

INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('Oakroot Nook', 'A rustic hobbit-hole beneath an oak tree, with hand-carved furniture and wildflower tea.', 60, 1, 'https://www.rentorshare.net/wp-content/uploads/2019/02/Five-bizarre-Airbnb-places-to-sleep.jpg');

INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('Fernwhistle Lodge', 'Secluded and serene, with birdsong in the morning and a pantry full of seed cake.', 68, 2, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoo8gB_uOVOi2XixtaUPw7eYv0TZ-l_9oZ04byH1I71tvxMhbgxgxMYoHiLSQcSEg0xkQ&usqp=CAU');

INSERT INTO spaces (name, description, price_per_night, owner_id, url) VALUES
('Thistleburrow', 'A bright, cheerful hobbit home with colorful quilts and a perfectly round breakfast table.', 72, 3, 'https://townsquare.media/site/96/files/2023/01/attachment-hobbit-house-airbnb.jpg?w=780&q=75');




INSERT INTO bookings (user_id, space_id, date, is_approved)
VALUES (1, 3, '2025-06-01', FALSE);

INSERT INTO bookings (user_id, space_id, date, is_approved)
VALUES (4, 6, '2025-06-15', FALSE);

INSERT INTO bookings (user_id, space_id, date, is_approved)
VALUES (2, 1, '2025-07-04', FALSE);

INSERT INTO bookings (user_id, space_id, date, is_approved)
VALUES (5, 7, '2025-07-21', FALSE);

INSERT INTO bookings (user_id, space_id, date, is_approved)
VALUES (3, 2, '2025-08-09', TRUE);
