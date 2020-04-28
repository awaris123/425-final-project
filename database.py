import sqlite3
import random
from datetime import datetime, timedelta

def connect():
    connection = sqlite3.connect('database.db')
    return connection

def create_new_employee(eid, first_name, last_name, ssn, job_type=0, salary=0, is_salaried=False):
    con = connect()
    con.cursor().execute('INSERT INTO Employee(EmployeeID, FirstName, LastName, SSN, Salary, IsSalaried, JobType) VALUES(?,?,?,?,?,?,?)', (eid, first_name, last_name, ssn, salary, is_salaried, job_type))
    con.commit()
    con.close()

def set_employee_salary(eid, salary, is_salaried):
    con = connect()
    con.cursor().execute('UPDATE Employee SET Salary=?, IsSalaried=? WHERE EmployeeID=?', (salary, is_salaried, eid))
    con.commit()
    con.close()

def get_employees(eids):
    # Build string list for query
    lst = str(eids[0])

    for i in range(1, len(eids)):
        lst += "," + str(eids[i])

    con = connect()
    cursor = con.cursor()

    cursor.execute('SELECT * FROM Employee WHERE EmployeeID IN (' + lst + ')')
    rows = cursor.fetchall()
    con.close()

    # Build list of tuples
    employees = list()

    for row in rows:
        employees.append(tuple(row))
    
    return employees

def create_new_customer(first_name, last_name):
    con = connect()
    con.cursor().execute('INSERT INTO Customer(FirstName, LastName) VALUES(?,?)', (first_name, last_name))
    con.commit()
    con.close()

def save_login_info(eid, privilege):
    con = connect()
    con.cursor().execute('INSERT INTO Login(EmployeeID, Privilege, LoginTime) VALUES(?,?,?)', (eid, privilege, datetime.now()))
    con.commit()
    con.close()

# We can store the LoginTime in the session so when the user logs out we can set the LogoutTime like this
def save_logout_info(eid, login_time):
    con = connect()
    con.cursor().execute('UPDATE Login SET LogoutTime=? WHERE EmployeeID=? AND LoginTime=?', (datetime.now(), eid, login_time))
    con.commit()
    con.close()

def register_inventory(model_number, cost, lead_time=timedelta(), category=0, quantity=0):
    con = connect()
    con.cursor().execute('INSERT INTO Inventory(ModelNumber, Cost, LeadTime, Category, Quantity) VALUES(?,?,?,?,?)', (model_number, cost, lead_time.total_seconds(), category, quantity))
    con.commit()
    con.close()

def register_new_model(model_number, cost, sale_price, lead_time=timedelta(), category=0, quantity=0):
    con = connect()
    cursor = con.cursor()

    # Create an entry in Inventory first
    register_inventory(model_number, cost, lead_time, category, quantity)

    # Get the assigned InventoryID
    cursor.execute('SELECT InventoryID FROM Inventory WHERE ModelNumber=?', (model_number,))
    row = cursor.fetchone()
    inventory_id = row[0]

    cursor.execute('INSERT INTO Model(ModelNumber, InventoryID, SalePrice) VALUES(?,?,?)', (model_number, inventory_id, sale_price))
    con.commit()
    con.close()

def update_inventory_quantity(model_number, quantity):
    con = connect()
    con.cursor().execute('UPDATE Inventory SET Quantity=? WHERE ModelNumber=?', (quantity, model_number))
    con.commit()
    con.close()

def create_new_order(customer_id, employee_id, model_number, sale_value):
    con = connect()
    con.cursor().execute('INSERT INTO CustomerOrder(CustomerID, EmployeeID, ModelNumber, SaleValue) VALUES(?,?,?,?)', (customer_id, employee_id, model_number, sale_value))
    con.commit()
    con.close()
