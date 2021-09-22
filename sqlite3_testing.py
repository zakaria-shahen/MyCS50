import sqlite3
    
conn = sqlite3.connect('javatpoint.db')  
print("Opened database successfully")  
  
conn.execute(''' INSERT INTO Employees (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Ajeet', 27, 'Delhi', 20000.00 )''')  
print("Table created successfully");  
  
conn.close()  