from flask import Flask, render_template, redirect, url_for, request, Response
import database
import random

app = Flask(__name__)



logged_in = {

}

permissions = {
    0:{
        "tables" : [],
        "views" : []
    },
    1:{
        "tables" : ['Employee'],
        "views" : []
    },
    2:{
        "tables" : ['CustomerOrder'],
        "views" : ['totalRevenue', 'customerModel']
    },
    3:{
        "tables" : ['Model'],
        "views" : ['partAvailability']
    },
    4:{
        "tables" : ['Customer', 'Employee', 'Login', 'Inventory', 'Model', 'CustomerOrder'],
        "views" : ['totalRevenue', 'customerModel', 'partAvailability', 'expenseReport']
    }

}
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/employee', methods=['POST'])
def signup():
    firstName = request.json["fname"]
    lastName = request.json["lname"]
    ssn = request.json["ssn"]
    eid = random.randint(100000, 999999)

    database.create_new_employee(eid, firstName, lastName, ssn)

    return url_for('get_eid', eID=eid)



@app.route('/eid/<eID>', methods=['GET'])
def get_eid(eID):
    return render_template('eid.html', eID=eID)


@app.route('/home/<eID>', methods=['GET'])
def homepage(eID):


    employee = database.get_employees([eID])[0]
    eid = int(employee["EmployeeID"])
    priv = employee["JobType"]
    print(priv)
    tables = permissions[priv]["tables"]
    views = permissions[priv]["views"]


    login_time = database.save_login_info(eid, priv)
    logged_in[eid] = login_time
    print(logged_in)

    return render_template('home.html', employee=employee, tables=tables, views=views)


@app.route('/table/<name>', methods=['GET'])
def get_table(name):
    ids = {
        "Customer":"CustomerID",
        "Employee":"EmployeeID",
        "Login":"EmployeeID",
        "Inventory":"InventoryID",
        "Model":"ModelNumber",
        "CustomerOrder":"OrderNumber"
    }
    eid = int(request.cookies.get('eID'))
    table = name
    id_column = ids[table]
    data = database.get(table, id_column)
    return render_template('table.html', data=data)


@app.route('/view/<name>', methods=['GET'])
def get_view(name):
    eid = int(request.cookies.get('eID'))
    view = database.get_view(name)
    return render_template('view.html', view=view)


@app.route('/logout', methods=['GET'])
def logout():
    eid = int(request.cookies.get('eID'))
    time = str(logged_in[eid])
    del logged_in[eid]
    print(logged_in)
    database.save_logout_info(eid, time)
    resp=Response()

    return redirect(url_for('index')), resp.delete_cookie("eID")

if __name__ == '__main__':
    app.run(debug=True)
