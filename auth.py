from bottle import get, request, post, response
from werkzeug.security import generate_password_hash, check_password_hash
from models import users, conn

app_key = "may the force be with you"

@get("/signup")
def signup_frontend():
    if request.get_cookie("username", secret=app_key):
        return {"msg":"User already logged in!"}
    return {"msg":"Post username and password!"}

@post("/signup")
def signup():
    if request.get_cookie("username", secret=app_key):
        return {"msg":"User already logged in!"}
    username = request.forms.get("username")
    password = request.forms.get("password")
    password = generate_password_hash(password)
    u = users.select().where(users.c.username == username)
    user = conn.execute(u).fetchone()
    if user:
        return {"msg":"User already exists!"}
    u = users.insert().values(username = username, password = password)
    conn.execute(u)
    return {"msg":"Signed up successfully!"}

@get("/login")
def login_frontend():
    if request.get_cookie("username", secret=app_key):
        return {"msg":"User already logged in!"}
    return {"msg":"Post username and password!"}

@post("/login")
def login():
    if request.get_cookie("username", secret=app_key):
        return {"msg":"User already logged in!"}
    username = request.forms.get("username")
    password = request.forms.get("password")
    u = users.select().where(users.c.username == username)
    user = conn.execute(u).fetchone()
    if user and check_password_hash(user.password, password):
        response.set_cookie("username",username, secret=app_key)
        return {"msg":"Logged in succesfully!"}
    return {"msg":"Check your username and password!"}

@get("/logout")
def logout():
    if request.get_cookie("username",secret=app_key):
        response.delete_cookie("username")
        return {"msg":"Logged out successfully!"}
    return {"msg":"User not logged in!"}