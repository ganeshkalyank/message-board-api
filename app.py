from bottle import run, get, post, request, response, route
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

engine = create_engine("sqlite:///database.db")
meta = MetaData()
app_key = "may the force be with you"

users = Table(
    "users", meta,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String)
)

posts = Table(
    "posts", meta,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("body", String),
    Column("user", Integer, ForeignKey("users.id"))
)

replies = Table(
    "replies", meta,
    Column("id", Integer, primary_key=True),
    Column("user", Integer, ForeignKey("users.id")),
    Column("post", Integer, ForeignKey("posts.id")),
    Column("body", String)
)

meta.create_all(engine)
conn = engine.connect()

@get("/")
def index():
    return {"msg":"Server is running!"}

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

@get("/posts/all")
def get_posts():
    p = posts.select()
    post_result = conn.execute(p).fetchall()
    post_list = []
    for post in post_result:
        post_list.append({
            "title":post.title,
            "body":post.body,
            "user":post.user
        })
    return {"posts":post_list}

@get("/posts/<n:int>")
def get_n_posts(n):
    p = posts.select()
    post_result = conn.execute(p).fetchmany(n)
    post_list = []
    for post in post_result:
        post_list.append({
            "title":post.title,
            "body":post.body,
            "user":post.user
        })
    return {"feed":post_list}

@get("/posts/id/<id:int>")
def get_post_by_id(id):
    p = posts.select().where(posts.c.id == id)
    post = conn.execute(p).fetchone()
    if post:
        return {"title":post.title,"body":post.body,"user":post.user}
    return {"msg":"Post not found!"}

@post("/posts/add")
def add_post():
    if request.get_cookie("username",secret=app_key):
        title = request.forms.get("title")
        body = request.forms.get("body")
        username = request.get_cookie("username",secret=app_key)
        u = users.select().where(users.c.username == username)
        user = conn.execute(u).fetchone()
        p = posts.insert().values(title = title, body = body, user = user.id)
        post = conn.execute(p)
        if post:
            return {"msg":"Post added successfully!"}
        return {"msg":"Failed to add post!"}
    return {"msg":"Login to add post!"}

@route("/posts/update/<id:int>", method="PATCH")
def edit_post(id):
    if request.get_cookie("username",secret=app_key):
        title = request.forms.get("title")
        body = request.forms.get("body")
        username = request.get_cookie("username",secret=app_key)
        u = users.select().where(users.c.username == username)
        user = conn.execute(u).fetchone()
        p = posts.select().where(posts.c.id == id)
        post = conn.execute(p).fetchone()
        if post.user == user.id:
            p_new = posts.update().where(posts.c.id == id).values(title = title,body = body)
            post_new = conn.execute(p_new)
            if post_new:
                return {"msg":"Post updated successfully!"}
            return {"msg":"Error updating the post!"}
        return {"msg":"Post created by other user!"}
    return {"msg":"Login to update post!"}

run(host="localhost",port=8080)