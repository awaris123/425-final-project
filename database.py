import sqlite3
import random
from datetime import datetime, timedelta

def connect():
    connection = sqlite3.connect('database.db')
    return connection

# General function to query data from any table and return the data as a list of dictionaries (with each entry being a row in the table)
def get(table, id_column, column_names, ids=None):
    con = connect()
    cursor = con.cursor()

    if ids is None: # Get all rows
        cursor.execute('SELECT * FROM ' + table)
    else: # Get specific ids
        # Build string list for query
        lst = str(ids[0])

        for i in range(1, len(ids)):
            lst += "," + str(ids[i])

        cursor.execute('SELECT * FROM ' + table + ' WHERE ' + id_column + ' IN (' + lst + ')')
    
    rows = cursor.fetchall()
    con.close()

    # Build list of dicts
    results = list()

    for row in rows:
        d = dict()
        i = 0

        # Assign each column a key from column_names
        for col in column_names:
            d[col] = row[i]
            i += 1

        results.append(d)
    
    return results


#------------------
#     Employee
#------------------

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

def get_employees(eids=None):
    return get("Employee", "EmployeeID", [
        "EmployeeID",
        "FirstName",
        "LastName",
        "SSN",
        "Salary",
        "IsSalaried",
        "JobType"
    ], eids)

#------------------
#     Customer
#------------------

def create_new_customer(first_name, last_name):
    con = connect()
    con.cursor().execute('INSERT INTO Customer(FirstName, LastName) VALUES(?,?)', (first_name, last_name))
    con.commit()
    con.close()

def get_customers(ids=None):
    return get("Customer", "CustomerID", [
        "CustomerID",
        "FirstName",
        "LastName"
    ], ids)

#------------------
#      Login
#------------------

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

#-------------------
#     Inventory
#-------------------

def register_inventory(model_number, cost, lead_time=timedelta(), category=0, quantity=0):
    con = connect()
    con.cursor().execute('INSERT INTO Inventory(ModelNumber, Cost, LeadTime, Category, Quantity) VALUES(?,?,?,?,?)', (model_number, cost, lead_time.total_seconds(), category, quantity))
    con.commit()
    con.close()

def update_inventory_quantity(model_number, quantity):
    con = connect()
    con.cursor().execute('UPDATE Inventory SET Quantity=? WHERE ModelNumber=?', (quantity, model_number))
    con.commit()
    con.close()

def get_inventory(ids=None):
    return get("Inventory", "InventoryID", [
        "InventoryID",
        "ModelNumber",
        "Cost",
        "LeadTime",
        "Category",
        "Quantity"
    ], ids)

#------------------
#      Model
#------------------

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

def get_models(model_numbers=None):
    return get("Model", "ModelNumber", [
        "ModelNumber",
        "InventoryID",
        "SalePrice"
    ], model_numbers)

#------------------
#      Order
#------------------

def create_new_order(customer_id, employee_id, model_number, sale_value):
    con = connect()
    con.cursor().execute('INSERT INTO CustomerOrder(CustomerID, EmployeeID, ModelNumber, SaleValue) VALUES(?,?,?,?)', (customer_id, employee_id, model_number, sale_value))
    con.commit()
    con.close()

def get_orders(order_numbers=None):
    return get("CustomerOrder", "OrderNumber", [
        "OrderNumber",
        "CustomerID",
        "EmployeeID",
        "ModelNumber",
        "SaleValue"
    ], order_numbers)

#------------------
#      Views
#------------------

def create_view(name, properties):
    tables_list = ""
    columns_list = ""

    # Construct a comma-seperated list of the tables and columns specified
    for table in properties:
        columns = properties[table]
        tables_list += table + ","

        for col in columns:
            columns_list += table + "." + col + ","
        
    # Remove trailing commas
    tables_list = tables_list[:-1]
    columns_list = columns_list[:-1]

    con = connect()
    con.cursor().execute('CREATE VIEW [' + name + '] AS SELECT ' + columns_list + ' FROM ' + tables_list)
    con.commit()
    con.close()
