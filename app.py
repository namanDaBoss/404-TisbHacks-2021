import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import time
from helpers import apology

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

# @app.route("/post/<string:post_slug>", methods=['GET'])
# def post_route(post_slug):
#     post = Posts.query.filter_by(slug=post_slug).first()
#     return render_template('post.html', params=params, post=post


@app.route("/edit/<id_slug>", methods=["GET", "POST"])
def edit(id_slug):
    """Editing product info"""
    if request.method == 'GET':
        row = db.execute(
            "SELECT * FROM products WHERE productid = :id", id=id_slug)
        print(row)

        outList = []
        outList.append(list((row[0]).values()))
        return render_template('edit.html', product=outList[0])
        # return render_template("edit.html")
    else:
        row = db.execute(
            "SELECT * FROM products WHERE productid = :id", id=id_slug)
        try:
            units = int(request.form.get("units"))
        except:
            units = row.get('units')
        try:
            location = int(request.form.get("location"))
        except:
            location = row.get('location')
        try:
            p_name = int(request.form.get("p_name"))
        except:
            p_name = row.get('p_name')
        try:
            seller_name = int(request.form.get("seller_name"))
        except:
            seller_name = row.get('seller_name')
        try:
            seller_phone = int(request.form.get("seller_phone"))
        except:
            seller_phone = row.get('seller_phone')
        try:
            seller_email = int(request.form.get("seller_email"))
        except:
            seller_email = row.get('seller_email')

        ntime = time.time()

        db.execute("UPDATE products SET p_name=p_name, seller_name=seller_name , units=units,seller_phone=seller_phone,seller_email=seller_email, location=location, time=time) WHERE productid = :prodid",
                   p_name=p_name, seller_name=seller_name, units=units, seller_email=seller_email, location=location, seller_phone=seller_phone, time=ntime, prodid=id_slug)
        # db.execute("UPDATE products SET units = :units WHERE productid = :prodid", units=units, prodid=prodid)
        return render_template('index.html')


def maps():
    """Opens location in google maps"""
    

@app.route("/add", methods=["GET", "POST"])
def add():
    """Adding new product"""
    if request.method == 'GET':
        return render_template("add.html")
    else:
        ntime = time.time()
        p_name = str(request.form.get("p_name"))
        seller_name = str(request.form.get("seller_name"))
        print(request.form.get('units'))
        units = int(request.form.get("units"))
        seller_phone = (request.form.get("seller_phone"))
        seller_email = str(request.form.get("seller_email"))
        location = str(request.form.get("location"))
        # product_desc = str(request.form.get("product_desc"))

        # add time remove product desc in db
        db.execute("INSERT INTO products(p_name,seller_name,units,seller_phone,seller_email, location, time) VALUES (:p_name, :seller_name, :units,:seller_phone, :seller_email,:location, :time)",
                   p_name=p_name, seller_name=seller_name, units=units, seller_email=seller_email, location=location, seller_phone=seller_phone, time=ntime)

        return render_template("index.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
