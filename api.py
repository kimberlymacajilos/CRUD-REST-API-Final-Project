from flask import Flask, make_response, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "admin"
app.config["MYSQL_DB"] = "company"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/employees", methods=["GET"])
def get_employees():
    data = data_fetch("""SELECT * FROM company.employee;""")
    return make_response(jsonify(data), 200)

@app.route("/employees/<int:ssn>", methods=["GET"])
def get_employees_by_ssn(ssn):
    data = data_fetch("""SELECT * FROM company.employee where ssn = {}""".format(ssn))
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
    cur.execute(""" DELETE FROM employee where ssn = %s""", (ssn))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"message": "employee deleted successfully", "row_affected": rows_affected}), 200)

if __name__ == "__main__":
    app.run(debug=True)
