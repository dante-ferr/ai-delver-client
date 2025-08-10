import logging
import dill
import base64
import httpx  # Use httpx instead of requests
from .listen_for_replays import listen_for_replays


async def send_training_request(level_data, server_url="http://localhost:8001"):
    """
    Orchestrates the entire process: sends a training request and then
    listens for the replay data.

    Args:
        level_data: The level object to be trained.
        server_url (str): The base URL of the AI server.
    """
    session_id = None
    try:
        # Step 1: Send the training request using an async HTTP client
        logging.info("Sending training request to the server...")
        payload = {"level": base64.b64encode(dill.dumps(level_data)).decode("ascii")}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{server_url}/train", json=payload, timeout=30.0
            )
            response.raise_for_status()  # Raise an exception for HTTP errors

            response_data = response.json()
            session_id = response_data.get("session_id")
            logging.info(f"Server responded: {response_data.get('message')}")

        if not session_id:
            logging.error("Failed to get a valid session_id from the server.")
            return

        # Step 2: Connect to the WebSocket and listen for replays
        replay_uri = f"ws://{server_url.split('//')[1]}/replay/{session_id}"

        async for replay_frame in listen_for_replays(uri=replay_uri):
            logging.info(f"Received replay frame: {replay_frame}")

    except httpx.RequestError as e:
        logging.error(f"HTTP request failed: {e}")
    except Exception as e:
        logging.error(f"An error occurred during the process: {e}")
