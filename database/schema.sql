drop table if exists user;
create table user (
    'id' INTEGER primary key,
    'username' TEXT not null,
    'password' TEXT not null
);

drop table if exists post;
create table post (
    'id' INTEGER primary key,
    'title' TEXT,
    'media' TEXT,
    'type' TEXT
);