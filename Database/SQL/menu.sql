CREATE TABLE menu (
    user text,
    day text,
    day_name text,
    meal text,
    dish text,
    PRIMARY KEY (user, day, meal, dish),
    FOREIGN KEY (user) REFERENCES user(email),
    FOREIGN KEY (meal) REFERENCES meal(title),
    FOREIGN KEY (dish) REFERENCES dish(code)
);