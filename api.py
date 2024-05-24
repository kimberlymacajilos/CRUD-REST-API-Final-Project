from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin"
app.config["MYSQL_DB"] = "company"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["JWT_SECRET_KEY"] = "secret"

mysql = MySQL(app)
jwt = JWTManager(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username == "test" and password == "test":
        access_token = create_access_token(identity={"username": username})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route("/employees", methods=["GET"])
def get_employees():
    data = data_fetch("""SELECT * FROM company.employee;""")
    return make_response(jsonify(data), 200)

@app.route("/employees/<int:ssn>", methods=["GET"])
def get_employees_by_ssn(ssn):
    data = data_fetch("""SELECT * FROM company.employee where ssn = {}""".format(ssn))
    return make_response(jsonify(data), 200)

@app.route("/dependents/<int:Essn>", methods=["GET"])
def get_dependentname_by_essn(Essn):
    data = data_fetch("""SELECT Dependent_name, Relationship FROM company.dependent where Essn = {}""".format(Essn))
    return make_response(jsonify(data), 200)

@app.route("/deptlocations", methods=["GET"])
def get_deptlocations():
    data = data_fetch("""SELECT * FROM company.dept_locations;""")
    return make_response(jsonify(data), 200)

@app.route("/workson/<int:Pno>", methods=["GET"])
def get_essn_hours(Pno):
    data = data_fetch("""SELECT Essn, Hours FROM company.works_on where Pno = {}""".format(Pno))
    return make_response(jsonify(data), 200)

@app.route("/project", methods=["GET"])
def get_project():
    data = data_fetch("""SELECT * FROM company.project;""")
    return make_response(jsonify(data), 200)

@app.route("/department", methods=["GET"])
def get_department():
    data = data_fetch("""SELECT * FROM company.department;""")
    return make_response(jsonify(data), 200)

@app.route("/employees", methods=["POST"])
def add_employee():
    cur = mysql.connection.cursor()
    info = request.get_json()
    ssn = info["ssn"]
    Fname = info["Fname"]
    Minit = info["Minit"]
    Lname = info["Lname"]
    Bdate = info["Bdate"]
    Address = info["Address"]
    Sex = info["Sex"]
    Salary = info["Salary"]
    Super_ssn = info["Super_ssn"]
    Dl_id = info["Dl_id"]
    cur.execute(
        """ INSERT INTO employee (ssn, Fname, Minit, Lname, Bdate, Address, Sex, Salary, Super_ssn, Dl_id) VALUE (%s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s)""", (ssn, Fname, Minit, Lname, Bdate, Address, Sex, Salary, Super_ssn, Dl_id)
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "employee added successfully", "row_affected": rows_affected}), 201)

@app.route("/employees/<int:ssn>", methods=["PUT"])
def update_employee(ssn):
    cur = mysql.connection.cursor()
    info = request.get_json()
    Fname = info["Fname"]
    Lname = info["Lname"]
    cur.execute(""" UPDATE employee SET Fname = %s, Lname = %s WHERE ssn = %s""", (Fname, Lname, ssn))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "employee updated successfully", "row_affected": rows_affected}), 200)

@app.route("/employees/<int:ssn>", methods=["DELETE"])
def delete_actor(ssn):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM company.employee where ssn = %s""", (ssn,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "employee deleted successfully", "row_affected": rows_affected}), 200)

@app.route("/employees/format", methods=["GET"])
def get_params():
    fmt = request.args.get('ssn')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)

if __name__ == "__main__":
    app.run(debug=True)
