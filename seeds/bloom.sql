-- Drop tables if they exist
DROP TABLE IF EXISTS user_plants CASCADE;
DROP TABLE IF EXISTS chats CASCADE;
DROP TABLE IF EXISTS help_requests CASCADE;
DROP TABLE IF EXISTS help_offers CASCADE;
DROP TABLE IF EXISTS plants CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Drop sequences if they exist
DROP SEQUENCE IF EXISTS chats_id_seq;
DROP SEQUENCE IF EXISTS users_id_seq;
DROP SEQUENCE IF EXISTS help_requests_id_seq;
DROP SEQUENCE IF EXISTS help_offers_id_seq;
DROP SEQUENCE IF EXISTS plants_id_seq;
DROP SEQUENCE IF EXISTS user_plants_id_seq;


-- Create sequence for users
CREATE SEQUENCE users_id_seq;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL, 
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password BYTEA NOT NULL,
    avatar_url_string VARCHAR(255), -- it will come as a string, in the future we will add the images to cloudinary 
    address VARCHAR(255)
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
    watering_frequency INT -- CHANGED THE WATER FREQUENCY TO INT
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
    id SERIAL PRIMARY KEY,
    recipient_id INT NOT NULL, 
    message TEXT[],
    date TIMESTAMP WITHOUT TIME ZONE,
    sender_id INT NOT NULL, 
    CONSTRAINT fk_user_sender FOREIGN KEY (sender_id) REFERENCES users (id),
    CONSTRAINT fk_user_recipient FOREIGN KEY (recipient_id) REFERENCES users (id)
);

-- Create sequence for chats
CREATE SEQUENCE help_requests_id_seq;
-- Create help_requests table
CREATE TABLE help_requests (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP WITHOUT TIME ZONE,
    title VARCHAR(255), 
    message VARCHAR(255), -- depending on requirements, could be TEXT type for longer messages
    start_date DATE, 
    end_date DATE,
    user_id INT,
    maxprice REAL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create sequence for chats
CREATE SEQUENCE help_offers_id_seq;
-- Create help_offers table
CREATE TABLE help_offers (
    id SERIAL PRIMARY KEY,
    message VARCHAR(255),
    status VARCHAR(255),
    user_id INT,
    bid REAL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id)
);


-- CREATE USER SEED --
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('user', '1', 'user1', 'user1@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'test_image1.png', 'test_address1');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('user', '2', 'user2', 'user2@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'test_image2.png', 'test_address2');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('user', '3', 'user3', 'user3@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'test_image3.png', 'test_address3');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('user', '4', 'user4', 'user4@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'test_image4.png', 'test_address4');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('user', '5', 'user5', 'user5@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'test_image5.png', 'test_address5');

-- CREATE PLANTS SEED --
INSERT INTO plants (common_name, latin_name, photo, watering_frequency) VALUES ('African sheepbush', 'Pentzia incana', 'plant_01.png', 2);
INSERT INTO plants (common_name, latin_name, photo, watering_frequency) VALUES ('Alder', 'Alnus. Black alder', 'plant_02.png', 1);
INSERT INTO plants (common_name, latin_name, photo, watering_frequency) VALUES ('Almond', 'Prunus dulcis', 'plant_03.png', 1);

-- CREATE USER PLANTS SEED --
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (1, 1, 3);
-- INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (1, 2, 2);

INSERT INTO chats (recipient_id, message, date, sender_id) VALUES (2, '{"Hello user 02"}', NOW(), 1);


INSERT INTO help_requests (date, title, message, start_date, end_date, user_id, maxprice) VALUES ('2023-10-19 10:23:54', 'title_01', 'message requesting help', '2023-02-01', '2023-03-01', 1, 50);
INSERT INTO help_requests (date, title, message, start_date, end_date, user_id, maxprice) VALUES ('2023-10-20 10:23:54', 'title_02', 'message requesting help 2', '2023-02-03', '2023-03-03', 2, 60);
INSERT INTO help_offers (message, status, user_id, bid) VALUES ('Offering help', 'pending', 1, '50');