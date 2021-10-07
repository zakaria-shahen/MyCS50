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



-- View Courses_time (realaion:(1-1) location courses - (M:M) groups and staff)
SELECT courses_time.id as "ID Time",
        courses.id as "ID course",
        courses.name as "Course Name",
        location.name as "location",
        day_week.name as "Day",
        courses_time.start_time_lecture as "Time Start",
        courses_time.end_time_lecture as "Time End",
        replace(group_concat(distinct(groups.name)), ",", ", ") as "Groups",
        replace(group_concat(distinct(staff.name)), ",", ", ") as "Staff"
        from courses_time 
left join courses on courses.id = courses_time.courses_modal
left join location on location.id = courses_time.location_
left join day_week on day_week.id = courses_time.week_
left join courses_time__staff on courses_time__staff.courses_time = courses_time.id
left join courses_time__groups on courses_time__groups.courses_time = courses_time.id
left join staff on staff.id = courses_time__staff.staff
left join groups on groups.id = courses_time__groups.group_
GROUP by courses_time.id;

-- Add Courses_time (3 Query)
insert into courses_time(courses_modal, location_, week_, start_time_lecture, end_time_lecture) values(?, ?, ?, ?, ?);
insert into courses_time__staff(courses_time, staff) values(?, ?);
insert into courses_time__groups(courses_time, group_) values(?, ?);

-- Edit Courses_time (5 Query)
update courses_time set courses_modal = ?, location_ = ?, week_ = ?, start_time_lecture = ?, end_time_lecture = ?  where id = ?;
delete from courses_time__staff where courses_time = ?", (id_courses_time, );
insert into courses_time__staff(courses_time, staff) values(?, ?);
delete from courses_time__groups where courses_time = ?", (id_courses_time, );
insert into courses_time__groups(courses_time, group_) values(?, ?);


-- Delete Courses_time (3 Query)
delete from courses_time__groups  where courses_time;
delete from courses_time__staff where courses_time;
delete from courses_time where id = ?;






-- View schedules (View)
select id, name from groups;

select  courses_time.id as "ID Time",
        courses.name as "courses name",
        location.name as "location",
        day_week.name as "Day",
        courses_time.start_time_lecture as "Start Time",
        courses_time.end_time_lecture as "End Time",
        replace(group_concat(DISTINCT staff.name), ",", ", ") as "Staff"
from courses_time
join courses on courses.id = courses_time.courses_modal
join location on location.id = courses_time.location_
join day_week on day_week.id = courses_time.week_
join courses_time__staff on courses_time__staff.courses_time = courses_time.id
join staff on staff.id = courses_time__staff.staff
join courses_time__groups on courses_time__groups.courses_time = courses_time.id
join groups on groups.id = courses_time__groups.group_
WHERE groups.id = ?
group by courses_time.id;
