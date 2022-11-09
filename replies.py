from bottle import post, request, get
from models import users, conn, replies

app_key = "may the force be with you"

@post("/reply/add/<id:int>")
def add_reply(id):
    if request.get_cookie("username",secret=app_key):
        body = request.forms.get("body")
        username = request.get_cookie("username",secret=app_key)
        u = users.select().where(users.c.username == username)
        user = conn.execute(u).fetchone()
        r = replies.insert().values(post=id,user=user.id,body=body)
        post = conn.execute(r)
        if post:
            return {"msg":"Reply added succesfully!"}
        return {"msg":"Error adding reply!"}
    return {"msg":"Login to reply!"}

@get("/reply/post/<id:int>")
def get_replies_by_post(id):
    r = replies.select().where(replies.c.post == id)
    reply_result = conn.execute(r).fetchall()
    reply_list = []
    for reply in reply_result:
        reply_list.append({
            "body":reply.body,
            "user":reply.user
        })
    return {"post_id":id,"replies":reply_list}