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
    stocks = db.execute("SELECT symbol, SUM(shares) as shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING shares > 0;",
                        session["user_id"])

    total_value = 0
    for stock in stocks:
        quote_data = lookup(stock["symbol"])
        stock["price"] = quote_data["price"]
        stock["total_value"] = stock["shares"] * stock["price"]
        total_value += stock["total_value"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]["cash"]

    grand_total = total_value + cash

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive integer for shares", 400)

        quote_data = lookup(request.form.get("symbol"))

        if not quote_data:
            return apology("symbol not found", 400)

        total_cost = float(shares) * quote_data["price"]

        cash = db.execute("SELECT cash FROM users WHERE id = ?;", session["user_id"])[0]["cash"]
        if cash < total_cost:
            return apology("not enough cash", 400)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total, transacted_at) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP);",
                   session["user_id"],
                   quote_data["symbol"],
                   shares,
                   quote_data["price"],
                   total_cost)

        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?;",
                   total_cost,
                   session["user_id"])
        flash("Buy successfully")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY transacted_at DESC;", session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?;", request.form.get("username")
        )
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        flash("Log in successfully")
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
        flash("Register successfully")
        return redirect("/")

    if request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "GET":
        # Get user's stocks that they can sell
        stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0;",
                            session["user_id"])
        return render_template("sell.html", stocks=stocks)
    elif request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        if not symbol or shares is None or shares <= 0:
            return apology("Invalid symbol or shares")

        user_shares = db.execute("SELECT COALESCE(SUM(shares), 0) as total_shares FROM transactions WHERE user_id = ? AND symbol = ?;",
                                 session["user_id"], symbol)[0]["total_shares"]

        if user_shares < shares:
            return apology("Not enough shares to sell")

        quote_data = lookup(symbol)
        price = quote_data["price"]

        total = price * shares

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?;", total, session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total) VALUES (?, ?, ?, ?, ?);",
                   session["user_id"], symbol, -shares, price, -total)

        flash("Sold successfully")

        return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        if not request.form.get("old_password"):
            return apology("must provide old password")

        if not request.form.get("new_password"):
            return apology("must provide new password")

        rows = db.execute("SELECT hash FROM users WHERE id = ?;", session["user_id"])

        if not check_password_hash(rows[0]["hash"], request.form.get("old_password")):
            return apology("incorrect old password")

        new_hash = generate_password_hash(request.form.get("new_password"))
        db.execute("UPDATE users SET hash = ? WHERE id = ?;", new_hash, session["user_id"])
        flash("Changed Password successfully")
        return redirect("/")
    else:
        return render_template("change_password.html")
