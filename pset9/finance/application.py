import os

from cs50 import SQL
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
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Query for all of users stocks
    user_stocks = db.execute("SELECT symbol, shares FROM stocks WHERE id = ?", int(session["user_id"]))
    length = len(user_stocks)
    stocks = []
    symbols = []
    names = []
    shares = []
    prices = []
    totals = []
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", int(session["user_id"]))
    final_total = user_cash[0]["cash"]

    # Find all stock data and put it inside of a list
    for i in range(length):
        stocks.insert(i, lookup(user_stocks[i]["symbol"]))
        symbols.insert(i, stocks[i]["symbol"])
        names.insert(i, stocks[i]["name"])
        shares.insert(i, user_stocks[i]["shares"])
        prices.insert(i, stocks[i]["price"])
        totals.insert(i, prices[i] * shares[i])
        final_total += totals[i]

    return render_template("index.html", length=length, symbols=symbols, names=names, shares=shares, prices=prices, totals=totals, cash=user_cash[0]["cash"], final_total=final_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Route if user submits buy form
    if request.method == "POST":
        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must enter in a symbol", 400)

        # Ensure symbol exists
        elif not lookup(request.form.get("symbol")):
            return apology("invalid symbol", 400)

        # Ensure number of shares is submitted
        elif not request.form.get("shares"):
            return apology("must enter in a number of shares wanted", 400)

        # Look up the symbol to find its name and price
        stock = lookup(request.form.get("symbol"))
        name = stock["name"]
        price = stock["price"]
        symbol = stock["symbol"]
        shares = int(request.form.get("shares"))
        cost = price * shares

        # Query for users cash value
        money = db.execute("SELECT cash FROM users WHERE id = ?", int(session["user_id"]))

        # Check to see if they can afford it
        if cost > money[0]["cash"]:
            return apology("the amount of shares specified is more than available funds", 400)

        # Deduct the amount from user table
        leftover = money[0]["cash"] - cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", leftover, int(session["user_id"]))

        # Add stock to history table
        db.execute("INSERT INTO history (id, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?)",
                   int(session["user_id"]), symbol, name, shares, price)

        # Query to see if user already own shares of that company
        own = db.execute("SELECT shares FROM stocks WHERE id = ? AND symbol = ?", int(session["user_id"]), symbol)

        # If user doesnt own any already insert into table
        if len(own) == 0:
            db.execute("INSERT INTO stocks (id, symbol, shares) VALUES(?, ?, ?)", int(session["user_id"]), symbol, shares)
            return redirect("/")

        # if user already owns add shares to existing ones and update table
        else:
            total_shares = own[0]["shares"] + shares
            db.execute("UPDATE stocks SET shares = ? WHERE id = ? and symbol = ?", total_shares, int(session["user_id"]), symbol)
            return redirect("/")

    # Shows buy page
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Query for users history
    user_stocks = db.execute("SELECT * FROM history WHERE id = ?", int(session["user_id"]))
    length = len(user_stocks)
    symbols = []
    names = []
    shares = []
    prices = []
    time = []

    # Find all stock data and put it inside of a list
    for i in range(length):
        symbols.insert(i, user_stocks[i]["symbol"])
        names.insert(i, user_stocks[i]["name"])
        shares.insert(i, user_stocks[i]["shares"])
        prices.insert(i, user_stocks[i]["price"])
        time.insert(i, user_stocks[i]["time"])

    return render_template("history.html", length=length, symbols=symbols, names=names, shares=shares, prices=prices, time=time)


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
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
    # Route if usesr submits quote form
    if request.method == "POST":
        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must enter in a symbol", 400)

        # Ensure symbol exists
        elif not lookup(request.form.get("symbol")):
            return apology("invalid symbol", 400)

        # Look up the symbol to find its name and price
        stock = lookup(request.form.get("symbol"))
        name = stock["name"]
        price = stock["price"]
        symbol = stock["symbol"]
        return render_template("quoted.html", name=name, price=price, symbol=symbol)

    # Shows quote page
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Route if user submits register form
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure conformation password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide conformation password", 400)

        # Ensure confirmation password is a match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        # Query database if username already exists
        old_user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if not len(old_user) == 0:
            return apology("username is taken", 400)

        # Add new user to database
        new_user = request.form.get("username")
        pass_hash = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", new_user, pass_hash)

        # Redirect user to login
        return redirect("/login")

    else:
        # Show register page
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Route if user sumbits sell form
    if request.method == "POST":
        # Ensure symbol is submitted
        if not request.form.get("symbol"):
            return apology("must select a symbol", 400)

        # Ensure shares is submitted
        if not request.form.get("shares"):
            return apology("must amount of shares", 400)
        # Query about user stocks
        user_stocks = db.execute("SELECT shares FROM stocks WHERE id = ? AND symbol = ?",
                                 int(session["user_id"]), request.form.get("symbol"))
        shares = user_stocks[0]["shares"]
        stocks = lookup(request.form.get("symbol"))
        price = stocks["price"]
        name = stocks["name"]

        # Ensure user only sells as much shares as they own
        if int(request.form.get("shares")) > shares:
            return apology("can't sell more shares than owned", 400)

        # Query for users cash value
        money = db.execute("SELECT cash FROM users WHERE id = ?", int(session["user_id"]))
        cash = money[0]["cash"] + price * int(request.form.get("shares"))

        # Update cash, stocks and history
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, int(session["user_id"]))
        db.execute("INSERT INTO history (id, symbol, name, shares, price) VALUES(?, ?, ?, ?, ?)",
                   int(session["user_id"]), request.form.get("symbol"), name, -int(request.form.get("shares")), price)

        # If user sells all the shares delete from stock table
        if shares == int(request.form.get("shares")):
            db.execute("DELETE FROM stocks WHERE id = ? and symbol = ?", int(session["user_id"]), request.form.get("symbol"))

        else:
            current_shares = shares - int(request.form.get("shares"))
            db.execute("UPDATE stocks SET shares = ? WHERE id = ? and symbol = ?",
                       current_shares, int(session["user_id"]), request.form.get("symbol"))

        return redirect("/")

    # Show sell page
    else:
        # Query for available stocks to sell
        user_stocks = db.execute("SELECT symbol, shares FROM stocks WHERE id = ?", int(session["user_id"]))
        length = len(user_stocks)
        stocks = []
        symbols = []
        shares = []

        for i in range(length):
            stocks.insert(i, lookup(user_stocks[i]["symbol"]))
            symbols.insert(i, stocks[i]["symbol"])
            shares.insert(i, user_stocks[i]["shares"])

        return render_template("sell.html", symbols=symbols, shares=shares, length=length)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():

    # Route if user submitted password form
    if request.method == "POST":
        # Ensure current password is submitted
        if not request.form.get("password1"):
            return apology("must enter current password", 400)

        # Ensure new password is submitted
        if not request.form.get("password2"):
            return apology("must enter new password", 400)

        # Ensure confirm password is submitted
        if not request.form.get("password3"):
            return apology("must confirm password", 400)

        # Ensure old password is correct
        user_pass = db.execute("SELECT * FROM users WHERE id = ?", int(session["user_id"]))
        if not check_password_hash(user_pass[0]["hash"], request.form.get("password1")):
            return apology("must enter correct old password", 400)

        # Ensure new password and confirm password matches
        if request.form.get("password2") != request.form.get("password3"):
            return apology("new password and confirm password must be the same", 400)

        # Update password hash
        newpass_hash = generate_password_hash(request.form.get("password2"))
        db.execute("UPDATE users SET hash = ? WHERE id = ?", newpass_hash, int(session["user_id"]))

        return redirect("/")

    # Show password page
    else:
        return render_template("password.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
