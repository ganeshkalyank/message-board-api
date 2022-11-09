from bottle import get, post, request, route
from models import posts, conn, users

app_key = "may the force be with you"

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

@route("/posts/delete/<id:int>", method="DELETE")
def delete_post(id):
    if request.get_cookie("username",secret=app_key):
        username = request.get_cookie("username",secret=app_key)
        u = users.select().where(users.c.username == username)
        user = conn.execute(u).fetchone()
        p = posts.select().where(posts.c.id == id)
        post = conn.execute(p).fetchone()
        if user.id == post.user:
            p_del = posts.delete().where(posts.c.id == id)
            post_del = conn.execute(p_del)
            if post_del:
                return {"msg":"Post deleted succesfully!"}
            return {"msg":"Error deleting post!"}
        return {"msg":"Post created by other user!"}
    return {"msg":"Login to delete post!"}