from flask import Flask, render_template, redirect, url_for, request, Response
import database
import random

app = Flask(__name__)



logged_in = {

}
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/employee', methods=['POST'])
def signup():
    ## This endpoint will be called when the user signs up from the index page
    ## logic needs to be implemnted to create a new employee in the databse here
    ## with all of the paramters from the request body
    ## and then redirect to get_eid page allowing them to sign in as the account they just created.
    ## We also need to generate and pass an to the eID endpoint
    ## redirect for some reason is currently broken
    print(request.json)
    firstName = request.json["fname"]
    lastName = request.json["lname"]
    ssn = request.json["ssn"]
    jobType = request.json["jobtype"]
    eid = random.randint(100000, 999999)

    database.create_new_employee(eid, firstName, lastName, ssn)

    return url_for('get_eid', eID=eid)



@app.route('/eid/<eID>', methods=['GET'])
def get_eid(eID):
    ## The endpoint will have to take in a paramter eID and display it
    ## the eid.html files needs a "go-to" button to the index page so
    ## the user can log in with the eID
    return render_template('eid.html', eID=eID)


@app.route('/home/<eID>', methods=['GET'])
def homepage(eID):


    employee = database.get_employees([eID])[0]
    eid = employee["EmployeeID"]
    priv = employee["JobType"]


    login_time = database.save_login_info(eid, priv)
    logged_in[eid] = login_time
    print(logged_in)


    ## This endpoint will be called from the index page, if the user logs in we will make an ajax request to this endpoint
    ## logic needs to be implemented to pull data from the database with the unique ID and populate into template and then
    ## to record the logged in session with the time
    ## from this template there needs to be a feature where the user can log out
    return render_template('home.html', employee=employee)


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
