from fastapi import FastAPI
from .routes import simulation
import threading
import uvicorn

app = FastAPI()
app.include_router(simulation.router, prefix="/simulation")

api_ready = threading.Event()


@app.on_event("startup")
def startup_event():
    api_ready.set()


def run_api():
    def _run_callback():
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", access_log=False)

    api_thread = threading.Thread(target=_run_callback, daemon=True)
    api_thread.start()
    return api_thread
