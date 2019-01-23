'''
Author: Ethen Spielmann IABM15c
Modul: 150
Project: First Rest-API project
File: Datasource file for Project with all DB-Related code
'''

import mysql.connector

# variables for easier editing later
db_name = 'rest_db'
usr_table = 'rest_user_table'

# method for connecting to db
def connect_to_db():
    global mydb
    global mycursor
    # connecting to mysql
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=""
    )

    # creating db cursor
    mycursor = mydb.cursor()
    use_db()

# method to check if database and table already exist
def check_for_db():
    db_there = False
    connect_to_db()
    mycursor.execute("SHOW DATABASES")
    for x in mycursor:
        if db_name in x:
          db_there = True
    return db_there

# method to switch to db easier
def use_db():
    mycursor.execute('USE ' + db_name)

# method to commit to db and close connection
def commit_db():
    mydb.commit()
    mydb.close()

# method to create db and tables if they dont exist
def create_db_and_tables():
    mycursor.execute('CREATE DATABASE ' + db_name)
    print "Created Database " + db_name + "..."
    use_db()
    print "Using Database " + db_name + "..."
    mycursor.execute('CREATE TABLE ' + usr_table + '(id INT AUTO_INCREMENT PRIMARY KEY, email varchar(255), name varchar(255), pass varchar(255))')
    commit_db()
    print "Created Table rest_user_table..."

if check_for_db() == False:
    create_db_and_tables()
    print "created DB: " + db_name

else:
    print db_name + " Already created..."

# method to insert a user into the db
def insert_user(email, name, password):
    connect_to_db()
    sql = "INSERT INTO " + usr_table + " (email, name, pass) VALUES (%s, %s, %s)"
    val = (email, name, password)
    mycursor.execute(sql, val)
    commit_db()
    print "User inserted"

# method to check if user exists in db
def check_user(name, password):
    connect_to_db()
    sql = "SELECT COUNT(*) FROM " + usr_table + " WHERE name = %s AND pass = %s"
    val = (name, password);
    mycursor.execute(sql, val)
    r = mycursor.fetchone()
    mydb.close()
    # result is the first and only return from db
    # but .fetchone() returns list so access via r[0]
    result = r[0]
    if result == 0:
        return False
    else:
        return True

# method to check if user exists in db
def check_user_exist(email, name):
    connect_to_db()
    sql = "SELECT COUNT(*) FROM " + usr_table + " WHERE email = %s OR name = %s"
    val = (email, name);
    mycursor.execute(sql, val)
    r = mycursor.fetchone()
    mydb.close()
    result = r[0]
    if result == 0:
        return False
    else:
        return True

# method to fetch user data from db
def get_user_data(name):
    connect_to_db()
    sql = "SELECT email, name, pass FROM " + usr_table + " WHERE name = '%s'" % name
    mycursor.execute(sql)
    r = mycursor.fetchall()
    mydb.close()
    result = r[0]
    userpass = ""
    email = result[0]
    username = result[1]
    userpass_r = result[2]
    for x in range(0, len(userpass_r)):
        userpass = userpass + '*'
    # saving fetched data as dictionary for easy transfering to main class
    data = {'Email': email, 'Username': username, 'Password': userpass}
    return data

# method to delete user from db
def delete_user(name):
    connect_to_db()
    sql = "DELETE FROM " + usr_table + " WHERE name = '%s'" % name
    mycursor.execute(sql)
    commit_db()

# method to update user from db
def update_user(oldname, newname, passw):
    connect_to_db()
    sql = "UPDATE " + usr_table + " SET name = '%s', pass = '%s' where name = '%s'" % (newname, passw, oldname)
    mycursor.execute(sql)
    commit_db()
    print "done"
