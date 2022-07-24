INSERT INTO customers(name, email, mobile) VALUES
('Sarah Rose', 'srose74@icloud.com', 0439998619),
('Harry Leonard', 'hleonard00@icloud.com', 0499999999);

INSERT INTO users (name, email, password) VALUES
('Immy Parsons', 'immy@icloud.com', 'password123');

INSERT INTO categories(category) VALUES
('Birthday'),
('Childrens Parties'),
('Baby Showers'),
('Custom Designs'),
('Special Person'),
('Halloween'),
('Holiday Cookies');

INSERT INTO cookies(name, image, price_in_cents, category_id) VALUES
('The Cowgirl', '/static/images/cookie-1-4.jpg', 450, 4),
('Sesame Street', '/static/images/cookie-2-2.jpg',600, 2),
('The birthday girl', '/static/images/cookie-3-1.jpg',500, 1),
('New baby girl', '/static/images/cookie-4-3.jpg',600, 3),
('The baby shower', '/static/images/cookie-5-3.jpg',600, 3),
('Just because', '/static/images/cookie-6-5.jpg',350, 5),
('Go Team', '/static/images/cookie-7-4.jpg',500, 4),
('The Big-0', '/static/images/cookie-8-1.jpg',500, 1),
('Hearts & Rainbows', '/static/images/cookie-9-2.jpg',500, 2);

INSERT INTO reviews(customer_id, cookie_id, tag_line, review, rating) VALUES
(1, 1, 'Supherb detail', 'My daughter is obsessed with all things cowgirl, so these cookies made her birthday very special. Thanks Immy for listening and creating these beautiful cookies.', 4),
(2, 6, 'Happy Anniversary', 'I was looking for a way to celebrate my first anniversary, with my girlfriend away, this was a beautiful way to let her know how I feel about her', 5);



