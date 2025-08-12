import logging
import dill
import base64
import httpx
from .listen_for_trajectories import listen_for_trajectories
from runtime.episode_trajectory import EpisodeTrajectoryFactory
from typing import cast
from level_loader import level_loader


async def send_training_request(server_url="http://localhost:8001"):
    """
    Orchestrates the entire process: sends a training request and then
    listens for the episode trajectory data.

    Args:
        level_data: The level object to be trained.
        server_url (str): The base URL of the AI server.
    """
    session_id = None
    try:
        # Step 1: Send the training request using an async HTTP client
        logging.info("Sending training request to the server...")
        payload = {
            "level": base64.b64encode(dill.dumps(level_loader.level)).decode("ascii")
        }

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

        # Step 2: Connect to the WebSocket and listen for episode trajectories
        trajectory_uri = (
            f"ws://{server_url.split('//')[1]}/episode-trajectory/{session_id}"
        )

        await listen_for_trajectories(uri=trajectory_uri)

        # async for trajectory_json in listen_for_trajectories(uri=trajectory_uri):
        #     trajectory_json = cast(str, trajectory_json)
        #     episode_trajectory = EpisodeTrajectoryFactory().from_json(trajectory_json)
        #     yield episode_trajectory

    except httpx.RequestError as e:
        logging.error(f"HTTP request failed: {e}")
    except Exception as e:
        logging.error(f"An error occurred during the process: {e}")
