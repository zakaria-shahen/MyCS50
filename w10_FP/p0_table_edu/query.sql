-- SQLite

-- View staff table
select 
    staff.id as "id",
    staff.name as "name",
    staff.short_name as "short name",
    staff_degree.name as "degree",
    departments.name as "department",
    colleges.name as "college"
    from staff
JOIN staff_degree on staff_degree.id = staff.degree
JOIN departments on departments.id = staff.department
join colleges on colleges.id = staff.college;

-- Edit staff
update staff set name = ?, short_name = ?, degree = ?, department = ?, college = ?   where id = ?;




-- View Courses table
SELECT courses.id as 'id',
        courses.name as 'Course Name',
        course_code as 'Code',
        level,
        term,
         group_type.name as 'Group Type'
    from courses
join group_type on group_type.id = courses.type;

-- Edit Courses
update courses set name = ?, course_code = ?, level = ?, term = ?, type = ? where id = ?;

-- Insert Courses
insert into courses(name, course_code, level, term, type) values(?, ?, ?, ?, ?)




-- View Groups
SELECT groups.id as "ID",
        groups.name,
        level,
        group_type.name as "type",
        departments.name as "department"
 from groups
join group_type on group_type.id = groups.type
join departments on departments.id = groups.department_id;

-- Insert Groups
insert into groups(name, lavel, type, department_id) values(?, ?, ?, ?)

-- Edit Courses
update groups set name = ?, level = ?, type = ?, department_id = ? where id = ?



-- View location
select * from location;

-- Insert location
insert into location(name) values(?)

-- Edit Location 
update location set name = ? where id = ?



-- View Groups
select groups.id as "ID",
        groups.name as "Name",
        level,
        group_type.name as "type",
        departments.name as "department"
 from groups
join group_type on group_type.id = groups.type
join departments on departments.id = groups.department;

-- Insert Groups
insert into groups(name, level, type, department) values(?, ?, ?, ?)

-- Edit Groups
update groups set name = ?, level = ?, type = ?, department = ? where id = ?




-- View courses_open
SELECT courses_open.id as "ID",
        courses.id as "ID course",
        courses.name as "Course Name",
        location.name as "location",
        day_week.name as "Day",
        courses_open.start_time_lecture as "Time Start",
        courses_open.end_time_lecture as "Time End"
    from courses_open 
join courses on courses.id = courses_open.id_course
join location  on location.id = courses_open.location_
join day_week on day_week.id = courses_open.week_;

-- Insert courses_open
insert into courses_open(id_course, location_, week_, start_time_lecture, end_time_lecture)
                values(?, ?, ?, ?, ?)

-- Edit courses_open
update courses_open set id_course = ?, location_ = ?, week_ = ?, start_time_lecture = ?, end_time_lecture = ? 
        where id  = ? 



-- View courses_time
SELECT courses_time.id as "ID Time",
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

-- Insert courses_time
insert into courses_time(courses_open, location_, week_, start_time_lecture, end_time_lecture)
                values(6, 2, 1, "03:00 AM", "04:00 AM");
select * from courses_open;

-- -- Edit courses_time
update courses_time set courses_open = ?, location_ = ?, week_ = ?, start_time_lecture = ?, end_time_lecture = ? 
        where id  = ? 



-- Insret courses_open__staff
insert into courses_open__staff(courses_open, staff)  values(3, 4);

-- Insert courses_time__groups
insert into courses_time__groups(courses_time, group_)  values(3, 2);

-- Edit courses_open__staff
update courses_open__staff set courses_open = ?, staff = ? where courses_open = ? and staff = ?;

-- Edit courses_time__groups
update courses_time__groups set courses_time = ?, group_id = ? where courses_time = ? and group_ = ?;
