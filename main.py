from bottle import get, run
from auth import *
from posts import *
from replies import *

@get("/")
def index():
    return {"msg":"Server is running!"}

run(host="localhost",port=8080)