from fastapi import FastAPI
from api_server.router import router
from api_server.db_connection import init_db
import logging
import sys

app = FastAPI()

app.include_router(router)

@app.on_event("startup")
def startup_event():
    # Configuring logging mode
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    
    # Initializates database by connecting to superuser and executing backup file
    init_db()