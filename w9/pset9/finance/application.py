import os
from dotenv import load_dotenv

import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db_name = "finance.db"

# Make sure API key is set
load_dotenv()
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    data = None
    cash = None

    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        # get stocks owner user
        cur.execute(
            "SELECT symbol, name, shares FROM users JOIN owner_stocks ON users.id = owner_stocks.id_user WHERE shares > 0 AND users.id = ?", (session["user_id"],))
        data = cur.fetchall()
        
        # get cash  
        cur.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"],))
        cash = float(format((cur.fetchall())[0][0], ".2f"))

    if not data:
        return render_template("index.html", rows=None, cash=cash, total=cash)

    # calc Price
    stocks = []
    total_Stocks_price = 0

    for row in data:
        info = lookup(row[0])
        if info == None:
            return apology("lookup(): Error API")

        new = {}
        new["symbol"] = row[0]
        new["name"] = row[1]
        new["shares"] = row[2]
        new["price"] = info["price"]
        total_Stocks_price += new["price"] * new["shares"]
        stocks.append(new)
        
    return render_template("index.html", rows=stocks, cash=cash, total=total_Stocks_price+cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        symbol = request.args.get("symbol")
        return render_template("buy.html", symbol=symbol)

    symbol = request.form.get("symbol")
    shares = request.form.get("shares")

    try:
        # (123.4 % 1) * 10 = 4.0000
        if not symbol or not shares or float(shares) <= 0 or round(float(shares) % 1 * 10) != 0:
            return apology(f"Error input symbol or shares")
    except: 
        return apology("Error input symbol or shares not number")

    shares = int(shares)

    # Check symbol    
    data = lookup(symbol)
    if data == None:
        flash("lookup(): not found symbol OR API Error")
        return redirect("/buy")
    
    symbol = data["symbol"]
    price = data["price"]
    name = data["name"]
    total = shares * price
    
    # check Cash
    cash = None
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        cur.execute("SELECT cash FROM users WHERE id = ?", (session["user_id"], ))
        cash = (cur.fetchall())[0][0]
    
    if cash < total:
        flash(f"Your cannot afford the number of shares at the current price.\n Total:{total} Cash: {cash}")
        return redirect("/buy")

    # Buy cash
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        # sum = format(cash - total, ".2f")
        cur.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (total, session["user_id"]))
        
        # check query Done 
        if cur.rowcount != 1:
            return apology("Error SQLite3: not change cash value")
        
        cur.execute("INSERT INTO transactions(id_user, type, symbol, price, shares) values(?, ?, ?, ?, ?)",
                    (session["user_id"], 1, symbol, price, shares))

        try:
            cur.execute("INSERT INTO owner_stocks(id_user, symbol, name, shares) values(?, ?, ?, ?)",
                        (session["user_id"], symbol, name, shares))
        except:
            cur.execute("UPDATE owner_stocks SET shares = shares + ? WHERE  id_user = ? AND symbol = ?",
                        (shares, session["user_id"], symbol))
        flash("Bought!")

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    if request.method == "GET":
        data = None
        
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("SELECT transactions.id, time_info, name, symbol, shares, price  from transactions join transactions_type on transactions.type = transactions_type.id;")
            data = cur.fetchall()
        
        return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = {}
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            username = request.form.get("username")
            cur.execute("SELECT * FROM users WHERE username = ?", (username, ))
            rows = cur.fetchall()
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)
    
        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        
        data = lookup(symbol)
        if data == None:
            flash("lookup(): not found symbol OR API Error")
            return redirect("/quote")

        name = data["name"]
        price = data["price"]
        symbol = data["symbol"]

        return render_template("quote.html", symbol=symbol, name=name, price=usd(price))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method != "POST":
        return render_template("register.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        flash("Please enter your password, username, or both")
        return redirect("/register")
   
    if request.form.get("password_again") != password:
        flash("Password and confirm password do not match")
        return redirect("/register")

    hash = generate_password_hash(request.form.get("password"))

    # save username into DB
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        # check exists user or not
        cur.execute("SELECT username FROM users WHERE username = ?", (username, ))
        if cur.fetchall():
            flash("Username already exists")
            return redirect("/register")
        
        # Add new user
        cur.execute("INSERT INTO users(username, hash) values(?, ?)", (username, hash))

    return redirect("/login")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        data = None

        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            cur.execute("SELECT symbol FROM owner_stocks WHERE id_user = ? AND shares > 0", (session["user_id"],))
            data = cur.fetchall()

        if len(data) == 0:
            data = 0
        
        symbol = request.args.get("symbol")
        shares = request.args.get("shares")

        return render_template("sell.html", data=data, symbol=symbol, shares=shares)
    
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        try:
            if not symbol or not shares or float(shares) <= 0 or round(float(shares) % 1 * 10) != 0:
                return apology("Error input symbol or shares")
        except: 
            return apology("Error input symbol or shares not number")

        # convert integer
        shares = int(shares)

        data = lookup(symbol)
        if data == None:
            flash("lookup(): Wrong symbol OR Error API")
            return redirect("/sell")

        total = data["price"] * shares

        with sqlite3.connect(db_name) as db:
            cur = db.cursor()

            try:
                # Check exitis symbol and shars count (SQL: check(shares >= 0) )
                cur.execute("UPDATE owner_stocks SET shares = shares - ? WHERE id_user = ?",
                            (shares, session["user_id"]))           
            except:
                flash("does not own any shares of that stock \n OR \n does not own that many shares of the stock.")
                return redirect("/sell")

            # sell symbol
            cur.execute("INSERT INTO transactions(id_user, type, symbol, price, shares) values(?, ?, ?, ?, ?)",
                        (session["user_id"], 2, symbol, total, shares))
            cur.execute("UPDATE users SET cash = cash + ? WHERE id = ?", (total, session["user_id"]))
        
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
