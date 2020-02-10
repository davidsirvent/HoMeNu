CREATE TABLE dish (
    user text,
    code text,
    title text,
    PRIMARY KEY (user, title),
    FOREIGN KEY (user) REFERENCES user(email)
);