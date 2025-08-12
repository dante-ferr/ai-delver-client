import websockets
import logging
from runtime.episode_trajectory import EpisodeTrajectoryFactory
from agent_loader import agent_loader
from typing import cast


async def listen_for_trajectories(uri="ws://localhost:8001/episode-trajectory"):
    """
    Connects to a WebSocket and yields received episode trajectory frames.

    This function is an async generator, which means it can be used
    in an 'async for' loop to process messages as they arrive.

    Args:
        uri (str): The WebSocket URI to connect to.

    Yields:
        The deserialized episode trajectory frame received from the server.

    Raises:
        Exception: Propagates exceptions from the WebSocket connection or message decoding.
    """
    logging.info(
        f"Connecting to WebSocket at {uri} to receive episode trajectory data..."
    )
    trajectory_factory = EpisodeTrajectoryFactory()

    try:
        # The 'async with' ensures the connection is properly closed
        async with websockets.connect(uri) as websocket:
            logging.info(
                "WebSocket connection established. Waiting for episode trajectory frames..."
            )

            # This loop waits for messages and yields them one by one
            async for trajectory_json in websocket:
                trajectory = trajectory_factory.from_json(cast(str, trajectory_json))
                trajectory.save(agent_loader.agent.name)

    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"WebSocket connection closed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred in WebSocket listener: {e}")
        # Re-raise the exception to be handled by the caller
        raise
