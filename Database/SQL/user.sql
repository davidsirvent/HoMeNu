CREATE TABLE user (
    email text,
    username text,
    pass text,
    activate_url text,
    reset_url text,
    accept_terms int,
    accept_pub int,
    PRIMARY KEY (email)
);