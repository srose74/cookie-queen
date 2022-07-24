CREATE DATABASE cookies_db;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    mobile INTEGER NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL
);

CREATE TABLE cookies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    image TEXT NOT NULL,
    price_in_cents INTEGER,
    category_id INTEGER REFERENCES categories(id)
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    cookie_id INTEGER REFERENCES cookies(id),
    tag_line TEXT NOT NULL,
    review TEXT NOT NULL,
    rating INTEGER
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_total INTEGER NOT NULL
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    cookie_id INTEGER REFERENCES cookies(id),
    quantity INTEGER NOT NULL,
    price_in_cents INTEGER NOT NULL
);


