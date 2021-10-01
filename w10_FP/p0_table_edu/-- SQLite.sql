-- SQLite

-- drop table courses_open;
-- drop table courses_open__staff;
-- drop table courses_open__groups;

-- create table courses_open(
--     id integer not null,
--     primary key (id),
--     foreign key (id) references courses(id)
-- );

-- create table courses_time(
--     id integer,
--     location_ integer not null ,
--     week_ integer not null,  
--     start_time_lecture varchar(15) not null,
--     end_time_lecture varchar(15),
--     courses_open integer not null,
--     primary key(id),
--     foreign key (location_) references location(id), 
--     foreign key (week_) references day_week(id), 
--     foreign key (courses_open) references courses_open(id)
-- );


-- create table courses_open__staff(
--     courses_open integer not null,
--     staff integer not null,
--     primary key(courses_open, staff),
--     foreign key(courses_open) references courses_time(id),
--     foreign key(staff) references staff(id)
-- );

-- create table courses_time__groups(
--     courses_time integer not null,
--     group_ integer not null,
--     primary key(courses_time, group_),
--     foreign key(courses_time) references courses_time(id),
--     foreign key(group_) references groups(id)
-- );




-- Insert Courses_open
-- insert into courses_open values(6);

-- select * from courses_open;





-- -- View courses_time
SELECT courses_time.id as "ID",
        courses.id as "ID course",
        courses.name as "Course Name",
        location.name as "location",
        day_week.name as "Day",
        courses_time.start_time_lecture as "Time Start",
        courses_time.end_time_lecture as "Time End",
        courses_open__staff.staff,
        courses_time__groups.group_
        -- staff.name,
        -- groups.name
    from courses_time 
join courses_open on courses_open.id = courses_time.courses_open
join courses on courses.id = courses_time.courses_open
join location on location.id = courses_time.location_
join day_week on day_week.id = courses_time.week_
join courses_open__staff on courses_open__staff.courses_open = courses_time.courses_open
join courses_time__groups on courses_time__groups.courses_time = courses_time.courses_open;
-- join staff on staff.id = courses_open__staff.staff
-- join groups on groups.id = courses_time__staff.group_;

-- -- Insert courses_time
-- insert into courses_time(courses_open, location_, week_, start_time_lecture, end_time_lecture)
--                 values(6, 2, 1, "03:00 AM", "04:00 AM");

-- delete from courses_time where id > 1;
-- select * from courses_time;



-- -- -- Edit courses_time
-- update courses_time set course_open = ?, location_ = ?, week_ = ?, start_time_lecture = ?, end_time_lecture = ? 
--         where id  = ? 


-- -- Insret courses_time__staff
-- insert into courses_open__staff(courses_open, staff)  values(6, 4);

-- SELECT * from courses_time__groups;
-- SELECT * from courses_open__staff;
-- SELECT * from courses_time;

-- -- Insert courses_time__groups
-- insert into courses_time__groups(courses_time, group_)  values(6, 2);

-- -- Edit courses_time__staff
-- update courses_time__staff set course_time = ?, staff = ? where course_time = ? and staff = ?;

-- -- Edit courses_time__groups
-- update courses_time__groups set course_time = ?, group_ = ? where course_time = ? and group_ = ?;
