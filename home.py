import os
import sys
from functools import wraps

from flask import render_template, request, Flask, session, redirect, url_for, flash
from flask_mysqldb import MySQL
from pandas import DataFrame

app = Flask(__name__)

#Below are the database configurations
app.config["Secret_Key"] = "6a79852e71abd3dc5e4d#"
#run_with_ngrok(app)
app.debug = True
# app.secret_key = "AsdHahD12@!#@3@#@#554"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSORD'] = ''
app.config["MYSQL_DB"] = 'aLma_acad'
app.config["SQLALCHEMY_DATABASE_URL"] = "http://localhost/phpmyadmin/tbl_structure.php?db=register&table=register"
app.config["MYSQL CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

#From here the app building starts

def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if "logged in" in session:
            return f(*args,**kwargs)
        else:
            flash("Unauthorized, Please log in ","Danger")
            return(redirect(url_for("home")))
    return wrap

@app.route("/",methods=["Post","Get"])
def home():



    return render_template("home.html")

@app.route("/markspage",methods=["POST","Get"])
def marks():
    try:
        con = mysql.connection.cursor()
        print("Connected to database")
    except Exception as e:
        sys.exit(e)

    con.execute("SELECT * FROM marks")
    data = DataFrame(data=con.fetchall())
    if request.method =="POST":
        name = request.form['name']
        rollno = request.form['rollno']
        mathmarks = request.form['mathmarks']
        phymarks = request.form['phymarks']
        chemmarks = request.form['chemmarks']
        total = request.form['total']
        percentage = request.form['percentage']

        con.execute("INSERT INTO marks (name,rollno,mathmarks,phymarks,chemmarks,total,percentage) VALUES ('{}',{},{},{},{},{},{})".format(name,rollno,mathmarks,phymarks,chemmarks,total,percentage))
        mysql.connection.commit()

        con.close()
        # flash("Submission successful")
    return render_template("markspage.html")
#Here start the route 2
@app.route("/leaderboard",methods=["Post","Get"])
def leaderboard():
    try:
        con = mysql.connection.cursor()
        print("Connected to database")
    except Exception as e:
        sys.exit(e)

    con.execute("SELECT * FROM marks")
    data = DataFrame(data=con.fetchall())
    if request.method =="POST":
        query = request.form.get("query",None)
        if query not in data:
            con.execute("SELECT * FROM marks WHERE (name LIKE '%{0}%') or (rollno LIKE '%{0}%') or (mathmarks LIKE '%{0}%') or"
                        "(phymarks LIKE '%{0}%') or (chemmarks LIKE '%{0}%') or (total LIKE '%{0}%') or (percentage LIKE '%{0}%')".format(query))
            Leaderboard = con.fetchall()
            return render_template('leaderboard.html',data_a = Leaderboard)
        else:
            flash("book not found")
    con.close()
    return render_template('leaderboard.html')


if __name__ == '__main__':
    #app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.run()
