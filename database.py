import sqlite3

def init():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    return cursor

def create_new_employee(first_name, last_name, ssn, job_type=0, salary=0, is_salaried=False):
    print(first_name)
    cursor.execute('INSERT INTO Employee(FirstName, LastName, SSN, Salary, IsSalaried, JobType) VALUES(?,?,?,?,?,?)', (first_name, last_name, 0, 0, 0, 0))
    connnection.commit()