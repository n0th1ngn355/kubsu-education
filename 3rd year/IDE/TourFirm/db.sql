drop table if exists Payments;
drop table if exists Tickets;
drop table if exists Seasons;
drop table if exists Tours;
drop table if exists CustInfo;
drop table if exists Customers;

create table Customers(
customer_id serial primary key,
lastname varchar(20) not null,
firstname varchar(20) not null,
midname varchar(20)
);

create table CustInfo(
customer_id int unique primary key REFERENCES Customers (customer_id) ON DELETE CASCADE,
pass_seria VARCHAR(10) not null,
city VARCHAR(30) not null,
county VARCHAR(30) not null,
phone_num VARCHAR(15) not null,
mail_index numeric(6) not null
);

create table Tours(
tour_id serial primary key,
name varchar(30) not null,
price money not null,
info text
);

create table Seasons(
season_id serial primary key,
tour_id int REFERENCES Tours (tour_id) ON DELETE CASCADE,
start_date timestamp NOT NULL DEFAULT NOW(),
end_date timestamp NOT NULL DEFAULT NOW(),
is_ended bool not null default false,
places_count numeric not null
);

create table Tickets(
ticket_id serial primary key,
customer_id int REFERENCES Customers (customer_id) ON DELETE CASCADE,
season_id int REFERENCES Seasons (season_id) ON DELETE CASCADE
);

create table Payments(
payment_id serial primary key,
ticket_id int REFERENCES Tickets (ticket_id) ON DELETE CASCADE,
payment_date timestamp NOT NULL DEFAULT NOW(),
summa money not null
);