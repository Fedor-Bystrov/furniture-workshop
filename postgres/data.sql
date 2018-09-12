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
