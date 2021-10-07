from os import EX_OSFILE
import sqlite3 

db_name = "table_edu.db"


def sql(query, values=(), return_data=False):
    """ return_data=False.. insert or update
        return_data=True select data... list[2]: 0-> keys  1-> values """
    
    if return_data == True:
        data = None
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("pragma foreign_keys = on")
            cur.execute(query, values)
            keys = [d[0] for d in cur.description]
            data = [keys, cur.fetchall()]
        return data
    
    else:
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute(query, values)


def view_table(query):
    """ view table """

    data = None
    try:
        data = sql(query, (), True)

    except:
        return "Error: SQLite3 Error view()"
    
    return data

def validations(data, condition, optionals=[]):
    """ data: data-> dict {key: snigle_value or list ()}
        condition: {name: type_condition}
        optionals: ["key String"] 
        return--> tuple Or nested_tuple Or string
         """

    verified_data = ()
    
    for key in condition:
        try:
            if type(data[key]) == list:
                data_list = list(map(int, data[key]))
                condition_list =  dict.fromkeys(range(len(data[key])), int)
                verified_list = validations(data_list, condition_list)
                verified_data += (verified_list, )
                continue              

            # Check not found keys optional
            if (not key in data and key in optionals) or not data[key]: # why 2 Condition 
            # if (not key in data and key in optionals) :
                verified_data += (None, )
                continue  
            
            # Convert str to int
            if condition[key] == int:
                data[key] = int(data[key])
            
            #  Check Values
            if type(data[key]) == condition[key]:
                # Important: When you use =+ a values order problem will occur
                verified_data += (data[key], )
            else:
                return f"{key} value is incorrect - input type: {type(data[key])}, expected type: {condition[key]}"
        except: 
            return "Not all required information has been entered"

    return verified_data

def add_edit_data(request_type, query, data, condition, optionals=[]):
    """ request_type: 1-> Add - 2-> Edit
        query: SQL update Or insert
        data: data-> {} 
        condition: {name: type_condition}
        optionals: ["key String"] 
        return--> string
        NOTE: (If Edit) Do not write the ID condition because it works with it automatically
        """

    # Check input Validation
    verified_data = validations(data, condition, optionals)

    if type(verified_data) == str:
        return verified_data

    if request_type == 2 and not "id" in data:
        return "The ID has not been entered"

    try:
        if request_type == 2:
            # Check ID validation
            id = int(data["id"])
            verified_data += (id, )

        # Query
        sql(query, verified_data) 
    except:
        if request_type == 2:
            return "Not all required information has been entered OR Incorrect ID number" 
        return "This name or other data already exists"
    
    if request_type == 2:
        return f"successfully data has been modified successfully - ID: {data['id']}"
    
    return f"successfully data has been modified successfully"
