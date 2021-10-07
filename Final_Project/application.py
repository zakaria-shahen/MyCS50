import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify, json, templating

from helpers import  view_table, sql, validations, add_edit_data


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure DB_name to use SQLite database
db_name = "table_edu.db"

# data static
data_static = {
    "group_type": ["Arabic", "English", "BIS", "FMI"],
    "colleges": ["FCBA"],
    "departments": ["General", "IS", "MB", "Acc"]
    # "staff_degree": ["Teaching Assistant", "Assistant Lecturer", "Lecturer / Assistant Professor", "Associate Professor", "Professor", "Professor Emeritus"],
    # "day_week": [],
}

@app.route("/")
def index():
    return redirect("/schedules")


# staff
@app.route("/staff", methods=["POST", "GET"])
def staff():
    """  """
    staff = view_table("""select
                            staff.id as "id",
                            staff.name as "name",
                            staff.short_name as "short name",
                            staff_degree.name as "degree",
                            departments.name as "department",
                            colleges.name as "college"
                            from staff
                        JOIN staff_degree on staff_degree.id = staff.degree
                        JOIN departments on departments.id = staff.department
                        join colleges on colleges.id = staff.college""")
    if type(staff) == str:
        return staff

    if request.method == "GET":
        return render_template("staff.html", keys=staff[0], data=staff[1])
    else:
        return render_template('functionals/data_view.html', keys=staff[0], data=staff[1],
                view_title="Staff Table", link_edit="/edit_staff", link_view="/staff", table="staff")

@app.route("/add_staff", methods=["POST"])
def add_staff():
    if request.method == "POST":
        # Check input Validation
        data = json.loads(request.get_data().decode('utf-8'))
        
        # Terms of Data Validation
        condition = {"name": str, "short_name": str, "degree": int, "department": int, "college": int}
        optionals = ["short_name"]

        # Query
        query = "INSERT INTO staff(name, short_name, degree, department, college) values(?, ?, ?, ?, ?)"

        # return f"{validations(condition, optionals)}"
        return add_edit_data(1, query, data, condition, optionals)

    else:
        return "Method POST only"

@app.route("/edit_staff", methods=["POST"])
def edit_staff():
    if request.method == "POST":
        # Check input Validation
        data = json.loads(request.get_data().decode("utf-8"))

        # Terms of Data Validation
        condition = {"name": str, "short_name": str, "degree": int, "department": int, "college": int}
        optionals = ["short_name"]

        # Query
        query = "update staff set name = ?, short_name = ?, degree = ?, department = ?, college = ?  where id = ?"
                                                # ('sdfghj', 'sd', 1, 2, 1, 2)
        return add_edit_data(2, query, data, condition, optionals)


# courses
@app.route("/courses", methods=["GET", "POST"])
def courses():
    courses = view_table("""SELECT courses.id as 'id',
                                    courses.name as 'Course Name',
                                    course_code as 'Code',
                                    level,
                                    term,
                                    group_type.name as 'Group Type',
                                    departments.name as 'department'
                                from courses
                                join group_type on group_type.id = courses.type
                                join departments on departments.id = courses.department""")
    

    if type(courses) == str:
        return courses

    if request.method == "GET":
        return render_template("courses.html", keys=courses[0], data=courses[1])
    else:
        return render_template('functionals/data_view.html', keys=courses[0], data=courses[1],
                view_title="courses Table", link_edit="/edit_course", link_view="/courses", table="courses")

@app.route("/add_course", methods=["POST"])
def add_course():
    if request.method == "POST":
        # Get and Convert Data
        data = json.loads(request.get_data().decode('utf-8'))

        # Terms of Data Validation
        condition = {"name": str, "course_code": str, "level": int, "term": int, "type": int, "department": int}

        # Query
        query = "INSERT INTO courses(name, course_code, level, term, type, department) values(?, ?, ?, ?, ?, ?)"

        return add_edit_data(1, query, data, condition)
    else:
        return "Method POST only"

@app.route("/edit_course", methods=["POST"])
def edit_course():
    if request.method == "POST":
        # Get input and Convert Data
        data = json.loads(request.get_data().decode('utf-8'))
        
        # Terms of Data Validation
        condition = {"name": str, "course_code": str, "level": int, "term": int, "type": int, "department": int}
        
        # Query update
        query = "update courses set name = ?, course_code = ?, level = ?, term = ?, type = ?, department = ? where id = ?"

        return add_edit_data(2, query, data, condition)




# Location
@app.route("/location", methods=["POST", "GET"])
def location():
    data = view_table("select * from location")
    if type(data) == str:
        return data
    
    if request.method == "GET":
        return render_template("location.html", keys=data[0], data=data[1])
    else:
        return render_template('functionals/data_view.html', keys=data[0], data=data[1],
                view_title="location Table", link_edit="/edit_location", link_view="/location", table="location")

@app.route("/add_location", methods=["POST"])
def add_location():
    if request.method == "POST":
        # Get Date form user
        data = json.loads(request.get_data().decode('utf-8'))
        
        # Terms of Data Validation
        condition = {"name": str}

        # Query
        query = "insert into location(name) values(?)"
        
        return add_edit_data(1, query, data, condition)

    else:
        return "Method POST only"

@app.route("/edit_location", methods=["POST"])
def edit_location():
    if request.method == "POST":
        # Check input Validation
        data = json.loads(request.get_data().decode("utf-8"))
        
        # Terms of Data Validation
        condition = {"name": str}

        # Query update
        query = "update location set name = ? where id = ?"

        return add_edit_data(2, query, data, condition)





# Groups
@app.route("/groups", methods=["POST", "GET"])
def groups():
    data = view_table("""select groups.id as "ID",
                                groups.name as "Name",
                                level,
                                group_type.name as "type",
                                departments.name as "department"
                        from groups
                        join group_type on group_type.id = groups.type
                        join departments on departments.id = groups.department """)
    if type(data) == str:
        return data
    
    if request.method == "GET":
        return render_template("groups.html", keys=data[0], data=data[1])
    else:
        return render_template('functionals/data_view.html', keys=data[0], data=data[1],
                view_title="Groups Table", link_edit="/edit_groups", link_view="/groups", table="groups")

@app.route("/add_groups", methods=["POST"])
def add_groups():
    if request.method == "POST":
        # Get and Convert Data
        data = json.loads(request.get_data().decode('utf-8'))

        # Terms of Data Validation
        condition = {"name": str, "level": int, "type": int, "department": int}

        # Query
        query = "INSERT INTO groups(name, level, type, department) values(?, ?, ?, ?)"

        return add_edit_data(1, query, data, condition)
    else:
        return "Method POST only"

@app.route("/edit_groups", methods=["POST"])
def edit_groups():
    if request.method == "POST":
        # Get input and Convert Data
        data = json.loads(request.get_data().decode('utf-8'))
        
        # Terms of Data Validation
        condition = {"name": str, "level": int, "type": int, "department": int}
        
        # Query update
        query = "update groups set name = ?, level = ?, type = ?, department = ? where id = ?"

        return add_edit_data(2, query, data, condition)




# courses_time
@app.route("/courses_time", methods=["POST", "GET"])
def courses_time():
    data = view_table("""SELECT courses_time.id as "ID Time",
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
                        GROUP by courses_time.id""")

    locations = sql("select * from location", (), True)[1]
    groups = sql("select id, name from groups", (), True)[1]
    staffs = sql("select id, name from staff", (), True)[1]
    courses = sql("select id, name from courses", (), True)[1]
    
    if request.method == "GET":
        return render_template("courses_time.html", keys=data[0], data=data[1], locations=locations, groups=groups, staffs=staffs, courses=courses)
    else:


        return render_template('functionals/data_view.html', keys=data[0], data=data[1],
                view_title="courses_time Table", link_edit="/edit_courses_time", link_view="/courses_time", table="courses_time")

@app.route("/add_courses_time", methods=["POST"])
def add_courses_time():
    if request.method == "POST":
        data = json.loads(request.get_data().decode('utf-8'))

        # validations data
        condition = {"courses_modal": int, "location_": int, "week_": int, "start_time_lecture": str, "end_time_lecture": str,
                        "staff": int, "group_": int}
        optional = ["end_time_lecture"]
        verified_data = validations(data, condition, optional)        
        staffs = verified_data[5]
        groups = verified_data[6]
        courses_time = verified_data[:5]


        if type(verified_data) == str:
            return verified_data
        # (1, 1, 1, '02:17', '05:17', (1, 2), (1, 2))
        
        # Insert data
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("pragma foreign_keys = on")
            cur.execute("begin transaction") 

            try:
                # insert courses_time 
                cur.execute("""insert into courses_time(courses_modal, location_, week_, start_time_lecture, end_time_lecture)
                                        values(?, ?, ?, ?, ?)""", courses_time)
                id_courses_time = cur.lastrowid
                
                # insert into staff and groups relation 
                ## if is single value
                if type(staffs) == int:
                    staffs = (staffs, )

                if type(groups) == int:
                    groups = (groups, )
                
                ## Query loop - It least One step
                for staff in staffs:
                    cur.execute("insert into courses_time__staff(courses_time, staff) values(?, ?)",
                                    (id_courses_time, staff))
                for group in groups:
                    cur.execute("insert into courses_time__groups(courses_time, group_) values(?, ?)",
                                    (id_courses_time, group))
                    
                cur.execute("commit")    
                cur.close()
                return "Succeeded in adding data"
            except: 
                # roll back change if Error
                cur.execute("rollback")
                cur.close()
                return "Error - No data has been added"

@app.route("/edit_courses_time", methods=["POST"])
def edit_courses_time():
    if request.method == "POST":
        data = json.loads(request.get_data().decode('utf-8'))


        condition = {"id": int, "courses_modal": int, "location_": int, "week_": int, "start_time_lecture": str, "end_time_lecture": str,
                        "staff": int, "group_": int}
        optional = ["end_time_lecture"]
        verified_data = validations(data, condition, optional)        
        
        if type(verified_data) == str:
            return verified_data


        id_courses_time = verified_data[0]
        data_courses_time = verified_data[1:6]
        data_staff = verified_data[6]
        data_groups = verified_data[7]

        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("pragma foreign_keys = on")
            cur.execute("begin transaction") 

            try:
                cur.execute("""update courses_time set courses_modal = ? , location_ = ?, week_ = ?, start_time_lecture = ?,
                                            end_time_lecture = ?  where id = ?""", data_courses_time + (id_courses_time, ))
                
                
                # delete all value staff wherer courses_time = ?
                cur.execute("delete from courses_time__staff where courses_time = ?", (id_courses_time, ))
                
                #  innsert new value staff
                if type(data_staff) == int:
                    cur.execute("insert into courses_time__staff(courses_time, staff) values(?, ?)",
                                    (id_courses_time, data_staff))
                else:
                    for staff in data_staff:
                        cur.execute("insert into courses_time__staff(courses_time, staff) values(?, ?)",
                                    (id_courses_time, staff))
                
        

                # delete all old value groups wherer courses_time = ?
                cur.execute("delete from courses_time__groups where courses_time = ?", (id_courses_time, ))
                
                #  innsert new value
                if  type(data_groups) == int:
                    cur.execute("insert into courses_time__groups(courses_time, group_) values(?, ?)",
                                    (id_courses_time, data_groups))
                else:
                    for group in data_groups:
                        cur.execute("insert into courses_time__groups(courses_time, group_) values(?, ?)",
                                        (id_courses_time, group))
                    
                cur.execute("commit")    
                cur.close()
                return "Data modification succeeded"
            except: 
                # roll back change if Error
                cur.execute("rollback")
                cur.close()
                return "Error - Not modified"





# schedules
@app.route("/schedules", methods=["POST", "GET"])
def schedules():
    if request.method == "GET":
        groups = sql("select id, name from groups", (), True)
        return render_template("schedules.html", values=groups[1])
    
    if request.method == "POST":
        id = json.loads(request.get_data().decode('utf-8'))

        data = sql("""select  courses_time.id as "ID Time",
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
                        group by courses_time.id""", (id, ), True)

        return render_template('functionals/data_view_readonly.html', keys=data[0], data=data[1], view_title="Schedules Table")


# search
@app.route("/search")
def search():
    """ Search by ID """
    if request.method == "GET":
        # Check input Validation  
        id = request.args.get("id")
        table = request.args.get("table")
        if not id or not table:
            return f"not input id OR not input table name {table} {id} {not id } { not table}"

        try:
            id = int(id)
        except:
            return "this is not id (int)"

        # Accese by users user_access_tables(id_user) => return list table access.. SOON
        access_tables = ["staff", "courses", "location", "groups", "courses_time", "courses_time__staf", "courses_time__groups"]
        if not table in access_tables:
            return "Table access: table name not found"
        

        table_join = ["courses_time"]

        # Query Data 
        data = None
        try:
            if not table in table_join:
                data = sql(f"select * from {table} where id = ?", (id,), True)

            elif table == "courses_time":
                data = sql("""SELECT courses_time.id as "id",
                                    courses_modal,
                                    location_,
                                    week_,
                                    start_time_lecture,
                                    end_time_lecture,
                                    group_concat(distinct group_) as "group_",
                                    group_concat(distinct staff) as "staff"
                            from courses_time 
                            left join courses_time__staff on courses_time__staff.courses_time = courses_time.id
                            left join courses_time__groups on courses_time__groups.courses_time = courses_time.id
                            GROUP by courses_time.id
                            having courses_time.id = ?""", (id,), True)
                
                # convert data two list to dict
                data = dict(zip(data[0], data[1][0]))
                
                # convert group and staff one strong to list int 
                data["group_"] = list(map(int, data["group_"].split(",")))
                data["staff"] = list(map(int, data["staff"].split(",")))
                
                return data            
            else:
                return f"the {table} is join and But there is no query for it"
        except:
            return f"id {id} not found OR Error sqlite3"

    return dict(zip(data[0], data[1][0]))
        

# delete_data
@app.route("/delete_data", methods=["POST"])
def delete_data():
    if request.method == "POST":
        # Check input Validation  
        data = json.loads(request.get_data().decode('utf-8'))
        id = data["id"]
        table = data["table"]
        if not id or type(id) != int:
            return "no input ID"
        
        if not table:
            return "no input table name"
        
        # Accese by users user_access_tables(id_user) => return list table access.. SOON
        access_tables = ["staff", "courses", "location", "groups", "courses_time"]
        if not table in access_tables:
            return "Table access: table name not found"


        table_join = ["courses_time"]

        # Query 
        with sqlite3.connect(db_name) as db: 
            cur = db.cursor()
            cur.execute("pragma foreign_keys = on")
            cur.execute("begin transaction")

            try: 
                if not table in table_join:
                    cur.execute(f"delete from {table} where id = ?", (id, ))    
                
                elif table == "courses_time":
                    cur.execute("delete from courses_time__groups  where courses_time = ?", (id, ))
                    cur.execute("delete from courses_time__staff where courses_time = ?", (id, ))
                    cur.execute("delete from courses_time where id = ? ", (id, ))
                
                cur.execute("commit")
                cur.close()
            
            except:
                cur.execute("rollback")
                cur.close()
                return(f"not found id: ID {id} or table: {table} - Or there is a foreign key")
            
        return f"Done: Delete ID {id} , name "
