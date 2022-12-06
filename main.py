from bottle import get, run
from auth import *
from posts import *
from replies import *

@get("/")
def index():
    response.status = 200
    return {"msg":"Server is running!"}

run(server="gunicorn")
