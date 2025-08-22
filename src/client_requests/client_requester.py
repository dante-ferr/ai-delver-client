import logging
import httpx
from level_loader import level_loader
from agent_loader import agent_loader
import websockets
from runtime.episode_trajectory import EpisodeTrajectoryFactory
from training_state_manager import training_state_manager
import json
from editor.components.overlay.message_overlay import MessageOverlay
from utils import json_to_sha256
import os

class ClientRequester:
    def __init__(self, server_url="localhost:8001"):
        self.server_url = server_url
        self.session_id: None | str = None

    async def send_training_request(self):
        """
        Sends a training request and then
        listens for the episode trajectory data.

        Args:
            level_data: The level object to be trained.
            server_url (str): The base URL of the AI server.
        """
        training_state_manager.sending_training_request = True
        try:
            uri = f"http://{self.server_url}/train"

            level_json = level_loader.level.to_dict()
            payload = {
                "level": level_json,
                "amount_of_episodes": training_state_manager.amount_of_episodes,
            }

            response_json = await self._send_request(uri, payload)
            logging.info(f"Server responded: {response_json.get('message')}")

            session_id = response_json.get("session_id")
            if session_id:
                self.session_id = session_id
                training_state_manager.sending_training_request = False
                training_state_manager.training = True
            else:
                logging.error("Failed to get a valid session_id from the server.")
                training_state_manager.reset_states()
                return

            # Each level configuration is saved with a unique hash as its filename, into the agent's directory.
            # This is done in order to allow the trajectories to point to a specific level configuration through
            # its specific hash. So when the trajectory is loaded to render a replay, the correct level will be
            # loaded as well.
            level_hash = level_loader.level.to_hash()
            level_path = (
                f"data/agents/{agent_loader.agent.name}/level_saves/{level_hash}.json"
            )
            if not os.path.exists(level_path):
                level_loader.level.save(level_path)

            await self.listen_for_trajectories(level_hash)

        except Exception as e:
            logging.error(f"An error occurred during the process: {e}")
            MessageOverlay(
                f"An error occurred during the process: {e}", subject="Error"
            )
            training_state_manager.reset_states()

    async def send_interrupt_training_request(self):
        """
        Sends a request to interrupt the training process.
        """
        try:
            training_state_manager.sending_interrupt_training_request = True

            uri = f"http://{self.server_url}/interrupt-training/{self.session_id}"

            response_json = await self._send_request(uri, {})
            logging.info(f"Server responded: {response_json.get('message')}")

            if response_json.get("success"):
                pass

        except Exception as e:
            logging.error(f"An error occurred during the process: {e}")
            MessageOverlay(
                f"An error occurred during the process: {e}", subject="Error"
            )
            training_state_manager.reset_states()

    async def _send_request(self, uri, payload):
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, json=payload, timeout=30.0)
            response.raise_for_status()

            response_data = response.json()
            logging.info(f"Server responded: {response_data.get('message')}")
            return response_data

    async def listen_for_trajectories(self, level_hash: str):
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
        if not self.session_id:
            raise ValueError("Session ID is not set.")

        uri = f"ws://{self.server_url}/episode-trajectory/{self.session_id}"

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
                async for response in websocket:
                    response_json = json.loads(response)

                    trajectory_data = response_json.get("trajectory")
                    is_end_signal = response_json.get("end")

                    if trajectory_data:
                        trajectory = trajectory_factory.from_json(trajectory_data)
                        trajectory.level_hash = level_hash
                        trajectory.save(agent_loader.agent.name)
                    elif is_end_signal:
                        training_state_manager.training = False
                        training_state_manager.sending_interrupt_training_request = (
                            False
                        )

        except websockets.exceptions.ConnectionClosed as e:
            logging.warning(f"WebSocket connection closed: {e}")
            training_state_manager.reset_states()
        except Exception as e:
            logging.error(f"An unexpected error occurred in WebSocket listener: {e}")
            training_state_manager.reset_states()
            raise


client_requester = ClientRequester()
