import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # user_portfolio = db.execute(
    #     "SELECT id, symbol, name, SUM(shares)  FROM trades WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0 ORDER BY price DESC", session["user_id"])

    # user_cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    # current_worth = 0
    # for stock in user_portfolio:
    #     stock_data = lookup(stock["symbol"])
    #     stock["currentprice"] = stock_data["price"]
    #     stock["totalprice"] = stock_data["price"] * stock["SUM(shares)"]
    #     current_worth += stock["totalprice"]
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Ensure shares was submitted and is a positive integer
        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive integer for shares", 400)

        # Look up the stock quote
        quote_data = lookup(request.form.get("symbol"))

        # Check if the symbol exists
        if not quote_data:
            return apology("symbol not found", 400)

        # Calculate the total cost
        total_cost = float(shares) * quote_data["price"]

        # Check if the user can afford the purchase
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
        if cash < total_cost:
            return apology("not enough cash", 400)

        # Insert the purchase into the database
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total, transacted_at) VALUES (:user_id, :symbol, :shares, :price, :total, CURRENT_TIMESTAMP)",
                    user_id=session["user_id"],
                    symbol=quote_data["symbol"],
                    shares=shares,
                    price=quote_data["price"],
                    total=total_cost)

        # Update the user's cash balance
        db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
                    total_cost=total_cost,
                    user_id=session["user_id"])

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        quote_data = lookup(request.form.get("symbol"))
        if not quote_data:
            return apology("invalid symbol", 400)
        return render_template("quoted.html", quote=quote_data)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif db.execute("SELECT COUNT(*) AS count FROM users WHERE username = ?;", request.form.get("username"))[0]["count"]:
            return apology("the username already exists", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("the passwords do not match.", 400)
        hash_password = generate_password_hash(request.form.get("password"))
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?);", request.form.get("username"), hash_password)
        session["user_id"] = id
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
