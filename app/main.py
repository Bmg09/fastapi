from fastapi import FastAPI
from . import model
from .database import engine
from . routers import post,user,auth,vote
from .config import settings
#what is cors? 
#CORS is a mechanism that uses additional HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin. 
# A web application executes a cross-origin HTTP request when it requests a resource that has a different origin (domain, protocol, or port) from its own.
from fastapi.middleware.cors import CORSMiddleware

description = """
This API helps you do awesome stuff. 🚀 like you create posts, view posts,update posts,delete them,Vote them.
## Items

You can **read items**.

## Users

You will be able to:

* **Create users** .
* **Read users** .
* **Login user**.
* **Create Post**.
* **Update Post**.
* **Delete Post**.
* **View Post**.

Some routes are protected unless you login you won't be able to access the data.
"""
# model.Base.metadata.create_all(bind=engine)
#fastapi app instance 
app = FastAPI(title="Simple Twitter like application",description=description)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#path operation matters here 
#if a path exists in multiple routers then the first path is used
#/path/{id} is same as /path/latest if a end point is matched like /path/123 then it is unable to find path and
#returns value is not valid int
#so to avoid error we need to set unparameterized path first and then parameterized path
#/path/latest first
#/path/{id} second


#pydantic validator for the request body 
#database connection realdictcursor is used to return the result as a dictionary with column names as keys

app.include_router(auth.router)    
app.include_router(user.router)
app.include_router(post.router)
app.include_router(vote.router)
#CRUD operations

#root path
@app.get("/")
async def root():
    return {"message": "Hello World!!"}

