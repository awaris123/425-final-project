from flask import Flask, render_template, redirect, url_for, request, jsonify
import random
import string


app = Flask(__name__)




def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

## using this as a dumb database to test logic, will
## implement databse layer later
dummy_data = {

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
    eID = randomString(14)
    firstName = request.json["fname"]
    lastName = request.json["lname"]
    jobType = request.json["jobtype"]
    ssn = request.json["ssn"]
    dummy_data[eID] = {
        "fname":firstName,
        "lname":lastName,
        "jobtype":jobType,
        "SSN":ssn
    }

    return url_for("get_eid", eID=eID)



@app.route('/eid/<eID>', methods=['GET'])
def get_eid(eID):
    return render_template('eid.html', eID=eID)


@app.route('/home/<eID>', methods=['GET'])
def homepage(eID):
    ## This endpoint will be called from the index page, if the user logs in we will make an ajax request to this endpoint
    ## logic needs to be implemented to pull data from the database with the unique ID and populate into template and then
    ## to record the logged in session with the time
    ## from this template there needs to be a feature where the user can log out
    return render_template('home.html', employee=employee)
    try:
        employee = dummy_data[eID]

    except:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
