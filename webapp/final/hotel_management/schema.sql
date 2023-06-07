CREATE TABLE guest (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE(email)
);

CREATE TABLE booking (
    id INTEGER NOT NULL AUTO_INCREMENT,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    guest_id INTEGER NOT NULL,
    room_type_id INTEGER NOT NULL,
    breakfast BOOLEAN NOT NULL,
    airport_pickup_time TIME NULL,
    reference_number VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE(reference_number)
);

CREATE TABLE room_type (
    id INTEGER NOT NULL AUTO_INCREMENT,
    description VARCHAR(50) NOT NULL,
    code VARCHAR(10) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (code)
);

INSERT INTO room_type (description, code) VALUES ("Single Room", "SINGLE");
INSERT INTO room_type (description, code) VALUES ("Double Room", "DOUBLE");

INSERT INTO guest (name, email) VALUES ("Anthony", "anthony@gmail.com");
INSERT INTO guest (name, email) VALUES ("Britney", "britney@yahoo.com");

INSERT INTO booking (check_in, check_out, guest_id, room_type_id, breakfast, reference_number)
VALUES ("2022-06-10", "2022-06-15", 1, 1, TRUE, "1234567890");

INSERT INTO booking (check_in, check_out, guest_id, room_type_id, breakfast, reference_number)
VALUES ("2022-06-18", "2022-07-02", 2, 2, FALSE, "0987654321");