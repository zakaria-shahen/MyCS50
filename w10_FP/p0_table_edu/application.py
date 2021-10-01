from os import EX_PROTOCOL
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify, json

from helpers import  view_table, sql, validations, add_edit_data
# from flask_session import Session
# from tempfile import mkdtemp
# from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
# from werkzeug.security import check_password_hash, generate_password_hash


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
    return render_template("index.html")


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


@app.route("/courses_time", methods=["POST", "GET"])
def courses_open():
    if request.method == "GET":
            data = view_table("""SELECT courses_time.id as "ID Time",
                                        courses.id as "ID course",
                                        courses.name as "Course Name",
                                        location.name as "location",
                                        day_week.name as "Day",
                                        courses_time.start_time_lecture as "Time Start",
                                        courses_time.end_time_lecture as "Time End",
                                        courses_open__staff.staff,
                                        courses_time__groups.group_
                                    from courses_time 
                                join courses_open on courses_open.id = courses_time.courses_open
                                join courses on courses.id = courses_time.courses_open
                                join location on location.id = courses_time.location_
                                join day_week on day_week.id = courses_time.week_
                                join courses_open__staff on courses_open__staff.courses_open = courses_time.courses_open
                                join courses_time__groups on courses_time__groups.courses_time = courses_time.courses_open""")
    

    if type(data) == str:
        return data

    if request.method == "GET":
        return render_template("courses_time.html", keys=data[0], data=data[1])
    else:
        return render_template('functionals/data_view.html', keys=data[0], data=data[1],
                view_title="courses_time Table", link_edit="/edit_courses_time", link_view="/courses_time", table="courses_time")


@app.route("/add_courses_time", methods=["POST"])
def add_coutses_time():
    if request.method == "POST":
        data = json.loads(request.get_data().decode('utf-8'))
        
        # check and insert into courses_open 
        query = "insert into courses_open values(?)"
        status = add_edit_data(1, query, data, {"id": int})
        
        if type(status) == str:
            return status

        # insert into courses_open__staff
        query = "insert into "

        # insert into courses_time
        
        
        # insert into courses_tiem__groups

        
        return f"{data}"
    

@app.route("/search")
def search():
    """ Search by ID """
    if request.method == "GET":
        # Check input Validation  
        id = request.args.get("id")
        table = request.args.get("table")
        if not id or not table:
            return f"not input id OR not input table name {table} {id}"

        try:
            id = int(id)
        except:
            return "this is not id (int)"

        # Accese by users user_access_tables(id_user) => return list table access.. SOON
        access_tables = ["staff", "courses", "location", "groups"]
        if not table in access_tables:
            return "Table access: table name not found"
        
        # Query Data 
        data = None
        try:
            data = sql(f"select * from {table} where id = ?", (id,), True)
        except:
            return f"id {id} not found OR Error sqlite3"

    return dict(zip(data[0], data[1][0]))
        

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
        access_tables = ["staff", "courses", "location", "groups"]
        if not table in access_tables:
            return "Table access: table name not found"

        # Query 
        try:
            sql(f"delete from {table} where id = ?", (id, ), False)    
        except:
            return(f"not found id: ID {id} or table: {table} - Or there is a foreign key")
            
        return f"Done: Delete ID {id} , name "