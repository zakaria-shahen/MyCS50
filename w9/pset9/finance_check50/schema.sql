/*
    SQLite3
    date: 24-09-2021
 */

CREATE TABLE users (
    id INTEGER,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00,
    PRIMARY KEY(id)
);

CREATE UNIQUE INDEX username ON users (username);


 /*  My Query */
create table transactions_type(
    id integer,
    name varchar(10),
    primary key(id)
);

INSERT INTO transactions_type(id, name) values(1, "Buy");
INSERT INTO transactions_type(id, name) values(2, "Sell");

create table transactions(
    id integer,
    id_user integer not null,
    type integer not null, /* 1-> Buy ||  2-> Sell*/
    symbol varchar(20) not null,
    price integer check(price > 0) not null,
    shares integer check(shares > 0) not null,
    time_info text default CURRENT_TIMESTAMP,
    primary key(id),
    foreign key (id_user) references users(id),
    foreign key (type) references transactions_type(id)
);


create table owner_stocks(
    id_user integer not null,
    symbol varchar(20) not null,
    name text not null,
    shares integer check(shares >= 0) not null,
    foreign key (id_user) references users(id),
    primary key(id_user, symbol)
);