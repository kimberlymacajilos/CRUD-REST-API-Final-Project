from flask import Flask, make_response, jsonify
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

if __name__ == "__main__":
    app.run(debug=True)
