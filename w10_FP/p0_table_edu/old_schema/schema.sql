
create table staff_degree(
    id integer,
    name text unique not null,
    primary key (id)
);

insert into staff_degree values(1, "Teaching Assistant");
insert into staff_degree values(2, "Assistant Lecturer");
insert into staff_degree values(3, "Lecturer / Assistant Professor");
insert into staff_degree values(4, "Associate Professor");
insert into staff_degree values(5, "Professor");
insert into staff_degree values(6, "Professor Emeritus");

create table departments(
    id integer,
    name text unique not null,
    primary key(name)
);

insert into departments values(1, "General");
insert into departments values(2, "IS");
insert into departments values(3, "MB");
insert into departments values(4, "Acc");

create table colleges(
    id integer,
    name text unique not null,
    primary key(id)
);

insert into colleges values(1, "FCBA");


create table staff(
    id integer,
    name text not null unique,
    short_name text unique,
    degree integer not null,
    department integer not null,
    college integer not null,
    primary key(id),
    foreign key (degree) references staff_degree(id),
    foreign key (department) references departments(id),
    foreign key (college) references colleges(id)
);


create table group_type(
    id integer,
    name varchar(10) unique not null,
    primary key(id)
); 

insert into group_type values(1, "Arabic");
insert into group_type values(2, "English");
insert into group_type values(3, "BIS");
insert into group_type values(4, "FMI");


create table courses(
    id integer,
    name text unique not null,
    course_code varchar(20) unique not null,
    term integer not null check(term == 1 or term == 2), 
    level integer not null check(level >= 1 and level <= 4 ),
    type integer not null,
    department integer not null,
    primary key (id),
    foreign key (type) references group_type(id),
    foreign key (department) references departments(id)
); 


create table location(
    id integer,
    name text unique,
    primary key (id)
);


create table groups(
    id integer,
    name text not null unique,
    level integer not null check(level >= 1 and level <= 4 ),
    type integer not null, 
    department integer not null,
    primary key (id),
    foreign key (type) references group_type(id),
    foreign key (department) references departments(id)
);


create table day_week(
    id integer,
    name varchar(10) not null unique,
    primary key(id)
);

insert into day_week values(1, "Sunday");
insert into day_week values(2, "Monday");
insert into day_week values(3, "Tuesday");
insert into day_week values(4, "Wednesday");
insert into day_week values(5, "Thursday");
insert into day_week values(6, "Friday");
insert into day_week values(7, "Saturday");


create table courses_open(
    id integer not null,
    primary key (id),
    foreign key (id) references courses(id)
);

create table courses_time(
    id integer,
    location_ integer not null ,
    week_ integer not null,  
    start_time_lecture varchar(15) not null,
    end_time_lecture varchar(15),
    courses_open integer not null,
    primary key(id),
    foreign key (location_) references location(id), 
    foreign key (week_) references day_week(id), 
    foreign key (courses_open) references courses_open(id)
);


create table courses_open__staff(
    courses_open integer not null,
    staff integer not null,
    primary key(courses_open, staff),
    foreign key(courses_open) references courses_time(id),
    foreign key(staff) references staff(id)
);

create table courses_time__groups(
    courses_time integer not null,
    group_ integer not null,
    primary key(courses_time, group_),
    foreign key(courses_time) references courses_time(id),
    foreign key(group_) references groups(id)
);

