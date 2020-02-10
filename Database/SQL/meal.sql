CREATE TABLE meal (
    user text,
    title text,
    background_color text,
    PRIMARY KEY (user, title),
    FOREIGN KEY (user) REFERENCES user(email)
);