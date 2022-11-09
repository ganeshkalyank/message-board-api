from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey

engine = create_engine("sqlite:///database.db")
meta = MetaData()

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