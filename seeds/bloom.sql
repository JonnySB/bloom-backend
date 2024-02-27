-- Drop tables if they exist
DROP TABLE IF EXISTS user_plants CASCADE;
DROP TABLE IF EXISTS chats CASCADE;
DROP TABLE IF EXISTS help_request CASCADE;
DROP TABLE IF EXISTS help_offers CASCADE;
DROP TABLE IF EXISTS plants CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop sequences if they exist
DROP SEQUENCE IF EXISTS chats_id_seq;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP SEQUENCE IF EXISTS help_request_id_seq;
DROP SEQUENCE IF EXISTS help_offers_id_seq;
DROP SEQUENCE IF EXISTS plants_id_seq;
DROP SEQUENCE IF EXISTS user_plants_id_seq;


-- Create sequence for users
CREATE SEQUENCE users_id_seq;

CREATE TABLE users (
    id INTEGER PRIMARY KEY DEFAULT nextval('users_id_seq'),
    firstname VARCHAR(255), 
    lastname VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255),
    avatar VARCHAR(255), -- it will come as a string, in the future we will add the images to cloudinary 
    address VARCHAR(255),
);

-- Create user_plants table
CREATE TABLE user_plants (
    user_id INT,
    plant_id INT,
    quantity INT, 
    PRIMARY KEY (user_id, plant_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_plant FOREIGN KEY (plant_id) REFERENCES plants (id)
);

-- Create sequence for chats
CREATE SEQUENCE chats_id_seq;
-- Create chats table
CREATE TABLE chats (
    received_from VARCHAR(255),
    sent_to VARCHAR(255), 
    message VARCHAR(255),
    date TIMESTAMP WITHOUT TIME ZONE -- date without the timezone..
    user_id INT,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create sequence for chats
CREATE SEQUENCE help_request_id_seq;
-- Create help_request table
CREATE TABLE help_request (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP WITHOUT TIME ZONE,
    title VARCHAR(255), 
    message VARCHAR(255), -- depending on requirements, could be TEXT type for longer messages
    daterange DATERANGE, -- assuming you want a range of dates
    user_id INT,
    maxprice MONEY,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create sequence for chats
CREATE SEQUENCE help_offers_id_seq;
-- Create help_offers table
CREATE TABLE help_offers (
    id SERIAL PRIMARY KEY,
    message VARCHAR(255),
    status BOOLEAN,
    user_id INT,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
);


-- Create sequence for chats
CREATE SEQUENCE plants_id_seq;
-- Create plants table
-- Create plants table
CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    common_name VARCHAR(255),
    latin_name VARCHAR(255),
    photo VARCHAR(255), -- it will come as a string, in the future we will add the images to cloudinary 
    watering_frequency VARCHAR(255) -- NOT SURE WHAT KIND OF DATE TYPE WE WILL BE USING HERE, MAYBE REQUIRED CHANGES IN THE FUTURE
);



 -- some date for testing purposes 
INSERT INTO users (firstname, lastname, username, email, hashed_password, avatar, address) VALUES ('user_firstname', 'user_lastname', 'user_01', 'user_01@gmail.com', 'userpassword', 'avatar.png', 'User House, Duke of Wellington Avenue, London, V6X0 7PG ');
INSERT INTO users (firstname, lastname, username, email, hashed_password, avatar, address) VALUES ('user_firstname', 'user_lastname', 'user_02', 'user_02@gmail.com', 'userpassword', 'avatar.png', 'User House, Duke of Wellington Avenue, London, V6X0 7PG ');
INSERT INTO chats (received_from, sent_to, message, date, user_id) VALUES ('user_01', 'user_02', 'hello user 01', '2023-10-19 10:23:54', 1);
INSERT INTO help_request (date, title, message, daterange, user_id, maxprice) VALUES ('2023-10-19 10:23:54', 'title_01', 'help request sent', '[2023-02-01, 2023-03-01]', 1, 50);
INSERT INTO help_offers (message, status, user_id) VALUES ('Offering help', TRUE, 1);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (1, 1, 3);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (1, 2, 2);
INSERT INTO plants (common_name, latin_name, photo, watering_frequency) VALUES ('African sheepbush', 'Pentzia incana', 'plant_01.png', 'two times a week');
INSERT INTO plants (common_name, latin_name, photo, watering_frequency) VALUES ('Alder', 'Alnus. Black alder', 'plant_02.png', 'one a week');
INSERT INTO plants (common_name, latin_name, photo, watering_frequency) VALUES ('Almond', 'Prunus dulcis', 'plant_03.png', 'once a month');

