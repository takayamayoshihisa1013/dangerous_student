from flask import Flask, render_template, redirect, session, url_for, request
import mysql.connector.charsets
import mysql.connector.connection
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import mysql.connector

app = Flask("__name__")
app.secret_key = "wow"

@app.route("/")
def root():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = False
    if request.method == "POST":
        
        id = request.form.get("id")
        password = request.form.get("password")
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            db="school"
        )
        
        cur = conn.cursor()
        
        cur.execute("""
                    SELECT name, grade, class
                    FROM teachers
                    WHERE id = %s AND password = %s
                    """, (id, password))
        
        teacher_data = cur.fetchone()
        print(teacher_data)
        if teacher_data:
        
            session["user_name"] = teacher_data[0]
            session["grade"] = teacher_data[1]
            session["class"] = teacher_data[2]
            
            return redirect("home")
        else:
            error = True
    return render_template("login.html", error = error)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        
        id = request.form.get("id")
        name = request.form.get("name")
        grade = request.form.get("grade")
        class_name = request.form.get("class")
        password = request.form.get("password")
        
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            db="school"
        )
        
        cur = conn.cursor()
        
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS teachers(
                        id VARCHAR(255),
                        name VARCHAR(255),
                        password VARCHAR(255),
                        grade INT,
                        class CHAR(10),
                        PRIMARY KEY(id)
                    )
                    """)
        
        cur.execute("INSERT INTO teachers(id, name, password, grade, class) VALUES(%s,%s,%s,%s,%s)",
                    (id, name, password, grade, class_name))
        
        session["user_name"] = name
        session["grade"] = grade
        session["class"] = class_name
        
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/home")
def home():
    print(session)
    return render_template("home.html")

if __name__ == "__main__":
    app.run(port=5000, threaded=True, debug=True)