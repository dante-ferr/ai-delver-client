from fastapi import FastAPI
from .router import router

app = FastAPI()

# Register the router
app.include_router(router)
