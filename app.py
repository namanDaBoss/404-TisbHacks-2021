import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import time

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
""" app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
"""

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///products1.db")


@app.route("/")
# @login_required
def index():
    """Shows available goods"""
    rows = db.execute("SELECT * FROM products")
    # print(rows)
    # print(str(rows[0]))
    # x = list(rows[0])
    # y = list(x[0])
    # print(str(y))
    res = list((rows[0]).values())[0]
    print(res)

    iter = 0
    outList = []
    for dict in rows:
        outList.append(list(dict.values()))

    return render_template("index.html", products=outList)

@app.route("/edit",methods=["GET", "POST"])
def edit():
    """Editing product info"""
    if request.method == 'GET':
        return render_template("edit.html")
    else:
        units = int(request.form.get("units"))
        prodid = int(request.form.get("prodid"))
        db.execute("UPDATE products SET units = :units WHERE product_id = :prodid", units=units, prodid=prodid)
        return render_template('edit.html')

def add():
    """Adding new product"""
    if request.method == 'GET':
        return render_template("add.html")
    else:
        time = time.time()
        p_name = str(request.form.get("p_name"))
        seller_name = str(request.form.get("seller_name"))
        units = int(request.form.get("units"))
        seller_phone = int(request.form.get("seller_phone"))
        seller_email = str(request.form.get("seller_email"))
        location = str(request.form.get("location"))
        product_desc = str(request.form.get("product_desc"))
        
        # add time remove product desc in db
        db.execute("INSERT INTO products(p_name,seller_name,units,seller_phone,seller_email,location, product_desc, time) VALUES (:p_name, :seller_name, :units,:seller_phone, :seller_email,:location, :product_desc, :time)", p_name=p_name, seller_name= seller_name, units=units,seller_email=seller_email, location=location, product_desc=product_desc, time=time)

        return render_template("add.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)