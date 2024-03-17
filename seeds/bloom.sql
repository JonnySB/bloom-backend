DROP TABLE IF EXISTS user_plants CASCADE;
DROP TABLE IF EXISTS chats CASCADE;
DROP TABLE IF EXISTS help_requests CASCADE;
DROP TABLE IF EXISTS help_offers CASCADE;
DROP TABLE IF EXISTS plants CASCADE;
DROP TABLE IF EXISTS users CASCADE;
-- Drop sequences if they exist
DROP SEQUENCE IF EXISTS user_plants_id_seq CASCADE;
DROP SEQUENCE IF EXISTS chats_id_seq CASCADE;
DROP SEQUENCE IF EXISTS help_requests_id_seq CASCADE;
DROP SEQUENCE IF EXISTS help_offers_id_seq CASCADE;
DROP SEQUENCE IF EXISTS plants_id_seq CASCADE;
DROP SEQUENCE IF EXISTS users_id_seq CASCADE;
-- Create sequence for users
CREATE SEQUENCE users_id_seq;
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password BYTEA NOT NULL,
    avatar_url_string VARCHAR(255),
    address VARCHAR(255)
);
-- Create sequence for plants
CREATE SEQUENCE plants_id_seq;
-- Create plants table
CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    plant_id INT UNIQUE NOT NULL,
    common_name VARCHAR(255),
    latin_name VARCHAR(255),
    photo VARCHAR(255),
    watering_frequency INT
);

-- Create user_plants table
CREATE TABLE user_plants (
    user_id INT NOT NULL,
    plant_id INT NOT NULL, 
    quantity INT NOT NULL,
    PRIMARY KEY (user_id, plant_id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_plant FOREIGN KEY (plant_id) REFERENCES plants(plant_id) 
);

CREATE SEQUENCE chats_id_seq;
-- Create chats table
CREATE TABLE chats (
    id SERIAL PRIMARY KEY,
    recipient_id INT NOT NULL, 
    message TEXT[],
    start_date TIMESTAMP WITHOUT TIME ZONE,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    receiver_username VARCHAR(255),
    sender_username VARCHAR(255),
    sender_id INT NOT NULL, 
    CONSTRAINT fk_user_sender FOREIGN KEY (sender_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_recipient FOREIGN KEY (recipient_id) REFERENCES users (id) ON DELETE CASCADE
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
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
CREATE SEQUENCE help_offers_id_seq;
-- Create help_offers table
CREATE TABLE help_offers (
    id SERIAL PRIMARY KEY,
    message VARCHAR(255),
    status VARCHAR(255),
    user_id INT,
    request_id INT,
    bid REAL,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_request FOREIGN KEY (request_id) REFERENCES help_requests (id) ON DELETE CASCADE
);


-- CREATE USER SEED --
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('Tom', 'Jones', 'tee-jay', 'tjones@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'https://res.cloudinary.com/dououppib/image/upload/v1708633707/MY_UPLOADS/aibxzxdpk6gl4u5xjgjg.jpg', 'test_address1');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('Jane', 'Smith', 'jane95', 'jsmith@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person4_kqdufy.jpg', 'test_address2');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('Jilly', 'Smith', 'sm1thi', 'jsmith2@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person2_jpuq5z.jpg', 'test_address3');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('Barbra', 'Banes', 'barn-owl58', 'bbanes@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'https://res.cloudinary.com/dououppib/image/upload/v1709830406/PLANTS/person1_jdh4xm.jpg', 'test_address4');
INSERT INTO users (first_name, last_name, username, email, hashed_password, avatar_url_string, address) VALUES ('Alice', 'Lane', 'laney', 'alane@email.com', '$2b$12$6Og77D1E.ObtWMOX9dw//.AJpsNFAR6/6E1OHputlDCUFRytgEQGq', 'https://res.cloudinary.com/dououppib/image/upload/v1709830407/PLANTS/person3_itrqub.jpg', 'test_address5');

-- CREATE PLANTS SEED --
INSERT INTO "public"."plants" ("plant_id", "common_name", "latin_name", "photo", "watering_frequency") VALUES
(1,'African sheepbush', 'Pentzia incana', 'https://res.cloudinary.com/dououppib/image/upload/v1709740425/PLANTS/African_sheepbush_lyorlf.jpg', 2),
(2,'Alder', 'Alnus. Black alder', 'https://res.cloudinary.com/dououppib/image/upload/v1709740428/PLANTS/Alder_jc4szc.jpg', 1),
(3,'Almond', 'Prunus dulcis', 'https://res.cloudinary.com/dououppib/image/upload/v1709740430/PLANTS/Almond_aikcyc.jpg', 1),
(4,'Bamboo', 'Fargesia', 'https://res.cloudinary.com/dououppib/image/upload/v1709740434/PLANTS/Bamboo_bkwm52.jpg', 1),
(5,'Barberry', 'Berberis', 'https://res.cloudinary.com/dououppib/image/upload/v1709740432/PLANTS/Barberry_copy_gseiuj.png', 1),
(6,'Bergamot', 'Monarda', 'https://res.cloudinary.com/dououppib/image/upload/v1709740426/PLANTS/Bergamot_k7ympf.jpg', 1);

-- CREATE USER PLANTS SEED --
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (1, 1, 3);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (1, 5, 2);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (1, 2, 3);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (2, 5, 2);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (2, 3, 3);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (3, 5, 2);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (3, 2, 3);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (4, 2, 5);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (5, 4, 10);
INSERT INTO user_plants (user_id, plant_id, quantity) VALUES (5, 5, 2);

INSERT INTO chats (recipient_id, message, start_date, end_date, receiver_username, sender_username, sender_id) VALUES (1, '{"{\"sender\": \"jane95\", \"message\": \"Hello tee-jay, how are you?\"}"}', '2024-01-31','2024-03-01', 'tee-jay', 'jane95', 2);

INSERT INTO help_requests (date, title, message, start_date, end_date, user_id, maxprice) 
VALUES 
('2023-10-19 10:23:54', 'Help needed whilst on holiday.', 'I am going on holiday for all of February - would love some help!', '2023-02-01', '2023-02-28', 1, 75),
('2023-11-12 08:45:21', 'Help required with plant care.', 'Looking for someone to water my plants while I am away.', '2023-03-05', '2023-03-10', 2, 100),
('2023-11-28 14:30:09', 'Need assistance with gardening.', 'Seeking help in maintaining my garden during my absence.', '2023-04-15', '2023-04-20', 3, 90),
('2023-12-07 11:20:35', 'Help wanted for plant care.', 'Require someone to water my indoor plants while I am out of town.', '2023-05-03', '2023-05-08', 4, 80),
('2023-12-20 09:55:47', 'Assistance needed with garden maintenance.', 'Looking for a reliable person to care for my garden while I am away.', '2023-06-12', '2023-06-18', 5, 70),
('2024-01-05 16:10:02', 'Plant watering help required.', 'Seeking someone to water my plants regularly during my vacation.', '2023-07-02', '2023-07-07', 1, 85),
('2024-01-15 13:40:19', 'Gardening assistance wanted.', 'Require help in maintaining my backyard garden for a few weeks.', '2023-08-20', '2023-08-25', 2, 95),
('2024-02-02 10:05:38', 'Plant care help needed urgently.', 'Looking for immediate assistance in watering my plants.', '2023-09-10', '2023-09-15', 3, 65),
('2024-02-14 07:30:55', 'Help needed with indoor plants.', 'Seeking someone to take care of my indoor plants for a short duration.', '2023-10-05', '2023-10-10', 4, 75),
('2024-02-28 15:20:10', 'Garden watering assistance required.', 'Require help in watering my garden while I am away.', '2023-11-22', '2023-11-27', 5, 60);

INSERT INTO help_offers (message, status, user_id, request_id, bid) 
VALUES 
('I can water your plants regularly during your vacation.', 'pending', 2, 6, 70),
('I am available to assist with your gardening needs.', 'pending', 3, 7, 85),
('I can provide immediate help with watering your plants.', 'pending', 4, 8, 60),
('I am experienced in caring for indoor plants and can help.', 'pending', 5, 9, 75),
('I can assist you with watering your garden.', 'pending', 1, 10, 65),
('I am available to help with your garden maintenance.', 'pending', 2, 1, 80),
('I can provide assistance in caring for your indoor plants.', 'pending', 3, 2, 55),
('I have gardening experience and can help with your garden.', 'pending', 4, 3, 90),
('I am willing to assist with your gardening needs.', 'pending', 5, 4, 75),
('I can take care of your plants while you are on holiday.', 'pending', 1, 5, 70),
('I am available to assist with your gardening needs.', 'pending', 2, 6, 85),
('I can water your plants regularly during your vacation.', 'pending', 3, 7, 70),
('I am experienced in caring for indoor plants and can help.', 'pending', 4, 8, 75),
('I can assist you with watering your garden.', 'pending', 5, 9, 65),
('I am available to help with your garden maintenance.', 'pending', 1, 10, 80),
('I can provide immediate help with watering your plants.', 'pending', 2, 1, 60),
('I am willing to assist with your gardening needs.', 'pending', 3, 2, 75),
('I have gardening experience and can help with your garden.', 'pending', 4, 3, 90),
('I can take care of your plants while you are on holiday.', 'pending', 5, 4, 70),
('I am available to assist with your gardening needs.', 'pending', 1, 5, 85);

