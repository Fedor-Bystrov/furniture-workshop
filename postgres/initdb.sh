#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
CREATE USER workshop;
CREATE DATABASE workshop;
GRANT ALL PRIVILEGES ON DATABASE workshop TO workshop;
ALTER USER workshop WITH encrypted password 'workshop';
ALTER USER workshop SET search_path TO workshop, public;
EOSQL

psql -v ON_ERROR_STOP=1 --username "workshop" --dbname "workshop" <<-EOSQL
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
  purchase_id      INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
  creation_time    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  cart_id          INT REFERENCES cart (cart_id) ON UPDATE CASCADE ON DELETE CASCADE,
  product_id       INT REFERENCES product (product_id) ON UPDATE CASCADE,
  quantity         INT NOT NULL CHECK (quantity >= 0) DEFAULT 1
);

INSERT INTO category (name) VALUES ('Мягкая мебель'),('Системы хранения'), ('Офисная Мебель');

INSERT INTO product (name, category_id, price, short_description, description) VALUES
  ('Кровать', '1', 11.1, 'short_description_1', 'description_1'),
  ('Диван', '1', 11.2, 'short_description_1', 'description_1'),
  ('Кресло', '1', 11.3, 'short_description_1', 'description_1'),
  ('Шкаф', '2', 12.1, 'short_description_1', 'description_1'),
  ('Тумба', '2', 12.2, 'short_description_1', 'description_1'),
  ('Полки', '2', 12.3, 'short_description_1', 'description_1'),
  ('Стол', '3', 13.1, 'short_description_1', 'description_1'),
  ('Стул', '3', 13.2, 'short_description_1', 'description_1'),
  ('Кресло-качалка', '3', 13.3, 'short_description_1', 'description_1');

INSERT INTO customer (first_name, last_name, middle_name, locale, email, phone) VALUES
  ('test_customer_first_name_1', 'test_customer_last_name_1', '', 'RU', 'test@test.ru', '111111'),
  ('test_customer_first_name_2', 'test_customer_last_name_2', '', 'RU', 'test@test.ru', '222222'),
  ('test_customer_first_name_3', 'test_customer_last_name_3', 'middle_name_test_3', 'RU', 'test@test.ru', '333333');

INSERT INTO cart(creation_time, customer_id, price, description, shipping_address) VALUES
  (now(), 1, 50000, 'description_1', 'shipping_address_1'),
  (now(), 2,  50000,'description_2','shipping_address_2'),
  (now(), 2, 100000,'description_3', 'shipping_address_3'),
  (now(), 3, 100000,'description_4', 'shipping_address_4');

INSERT INTO purchase (cart_id, product_id, quantity) VALUES
  (1, 1, 10),
  (1, 4, 1),
  (1, 8, 54),
  (2, 3, 13),
  (2, 9, 12),
  (2, 4, 34),
  (3, 7, 17),
  (3, 2, 15),
  (3, 6, 10);
EOSQL
