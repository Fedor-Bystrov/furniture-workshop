CREATE TABLE category (
  category_id   INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  name          VARCHAR(60) NOT NULL UNIQUE
);

CREATE TYPE CUSTOMER_LOCALE AS ENUM ('RU', 'ENG');
CREATE TABLE customer (
  customer_id      INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  creation_time    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  first_name       VARCHAR(60) NOT NULL,
  last_name        VARCHAR(60) NOT NULL,
  middle_name      VARCHAR(60)              DEFAULT '',
  locale           CUSTOMER_LOCALE NOT NULL DEFAULT 'RU',
  email            VARCHAR(60) NOT NULL,
  phone            VARCHAR(60) NOT NULL
);

CREATE TABLE product (
  product_id        INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  name              VARCHAR(200)   NOT NULL UNIQUE,
  category_id       INT REFERENCES category (category_id),
  creation_time     TIMESTAMP  NOT NULL  DEFAULT CURRENT_TIMESTAMP,
  price             NUMERIC(10, 2) NOT NULL CHECK (price >= 0) DEFAULT 0,
  short_description VARCHAR(240) NOT NULL,
  description       TEXT NOT NULL
);

CREATE TABLE cart (
  cart_id          INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  creation_time    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  customer_id      INT REFERENCES customer   (customer_id),
  price            NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
  description      VARCHAR(240) NOT NULL,
  shipping_address TEXT NOT NULL
);

CREATE TABLE purchase (
  creation_time    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  cart_id          INT REFERENCES cart (cart_id) ON UPDATE CASCADE ON DELETE CASCADE,
  product_id       INT REFERENCES product (product_id) ON UPDATE CASCADE,
  quantity         INT NOT NULL CHECK (quantity >= 0) DEFAULT 1
);
