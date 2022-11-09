from bottle import get, request, post, response
from werkzeug.security import generate_password_hash, check_password_hash
from models import users, conn

app_key = "may the force be with you"

@get("/signup")
def signup_frontend():
    if request.get_cookie("username", secret=app_key):
        response.status = 403
        return {"msg":"User already logged in!"}
    response.status = 405
    return {"msg":"Post username and password!"}

@post("/signup")
def signup():
    if request.get_cookie("username", secret=app_key):
        response.status = 403
        return {"msg":"User already logged in!"}
    username = request.forms.get("username")
    password = request.forms.get("password")
    password = generate_password_hash(password)
    u = users.select().where(users.c.username == username)
    user = conn.execute(u).fetchone()
    if user:
        response.status = 403
        return {"msg":"User already exists!"}
    u = users.insert().values(username = username, password = password)
    conn.execute(u)
    response.status = 201
    return {"msg":"Signed up successfully!"}

@get("/login")
def login_frontend():
    if request.get_cookie("username", secret=app_key):
        response.status = 403
        return {"msg":"User already logged in!"}
    response.status = 405
    return {"msg":"Post username and password!"}

@post("/login")
def login():
    if request.get_cookie("username", secret=app_key):
        response.status = 403
        return {"msg":"User already logged in!"}
    username = request.forms.get("username")
    password = request.forms.get("password")
    u = users.select().where(users.c.username == username)
    user = conn.execute(u).fetchone()
    if user and check_password_hash(user.password, password):
        response.set_cookie("username",username, secret=app_key)
        response.status = 200
        return {"msg":"Logged in succesfully!"}
    response.status = 401
    return {"msg":"Check your username and password!"}

@get("/logout")
def logout():
    if request.get_cookie("username",secret=app_key):
        response.delete_cookie("username")
        response.status = 200
        return {"msg":"Logged out successfully!"}
    response.status = 401
    return {"msg":"User not logged in!"}