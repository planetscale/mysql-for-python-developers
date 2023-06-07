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