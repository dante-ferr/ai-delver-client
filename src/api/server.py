from fastapi import FastAPI
from .routes import simulation

app = FastAPI()
app.include_router(simulation.router, prefix="/simulation")
