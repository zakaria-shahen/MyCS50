import sqlite3

with sqlite3.connect("testing.db") as db:
    cur = db.cursor()
    try:
        cur.execute("insert into name(id, name) values(1, 'zakaria')")
        print("try")
    except:
        cur.execute("insert into name(id, name) values(5, 'omar')")
        print('1')


print("Done")
