import logging
import httpx
from loaders import level_loader
from loaders import agent_loader
from ._trajectory_listener import TrajectoryListener
from state_managers import training_state_manager
from app.components.overlay.message_overlay import MessageOverlay
import os
import time


class ClientRequester:
    """
    Handles all client-side requests to the AI training server, including
    initiating training, interrupting training, and listening for results
    via WebSockets.
    """
    def __init__(self, server_url="localhost:8001"):
        self.server_url = server_url
        self.session_id: None | str = None
        self.start_time: float = 0.0

    async def initial_request(self):
        """Pings the server for the first time to get relevant initial data."""
        try:
            uri = f"http://{self.server_url}/init"
            response_json = await self._send_get_request(uri)

            training_state_manager.set_value(
                "env_batch_size", response_json.get("env_batch_size")
            )
            training_state_manager.set_value("connected_to_server", "yes")

            return True

        except Exception as e:
            training_state_manager.set_value("connected_to_server", "no")

            return False

    async def send_training_request(self):
        """
        Initiates the training session.
        """
        training_state_manager.sending_training_request = True
        try:
            payload = self._create_training_payload()
            uri = f"http://{self.server_url}/train"

            response_json = await self._send_post_request(uri, payload)

            if not self._handle_training_response(response_json):
                return

            level_hash = self._ensure_level_saved()

            if not self.session_id:
                raise ValueError("No session ID received from the server.")

            listener = TrajectoryListener(
                self.server_url, self.session_id, self.start_time
            )
            await listener.listen(level_hash)

        except Exception as e:
            self._handle_error(e)

    async def send_interrupt_training_request(self):
        """
        Sends a request to interrupt the current training session on the server.
        """
        try:
            training_state_manager.sending_interrupt_training_request = True

            uri = f"http://{self.server_url}/interrupt-training/{self.session_id}"

            response_json = await self._send_post_request(uri, {})

            if response_json.get("success"):
                pass

        except Exception as e:
            self._handle_error(e)

    def _create_training_payload(self) -> dict:
        level_json = level_loader.level.to_dict()
        return {
            "level": level_json,
            "amount_of_cycles": training_state_manager.amount_of_cycles,
            "episodes_per_cycle": training_state_manager.episodes_per_cycle,
        }

    def _handle_training_response(self, response_json: dict) -> bool:
        session_id = response_json.get("session_id")
        if session_id:
            self.session_id = session_id
            training_state_manager.sending_training_request = False
            training_state_manager.training = True
            self.start_time = time.time()
            return True
        else:
            logging.error("Failed to get a valid session_id from the server.")
            training_state_manager.reset_states()
            return False

    def _ensure_level_saved(self) -> str:
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
        return level_hash

    def _handle_error(self, e: Exception):
        logging.error(f"An error occurred during the process: {e}")
        MessageOverlay(f"An error occurred during the process: {e}", subject="Error")
        training_state_manager.reset_states()

    async def _send_get_request(self, uri) -> dict:
        """
        A helper method to send a GET request to the server.

        Args:
            uri (str): The full URI for the request.

        Returns:
            The JSON response from the server as a dictionary.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(uri, timeout=30.0)
            return self._get_response_data(response)

    async def _send_post_request(self, uri, payload) -> dict:
        """
        A helper method to send a POST request to the server.

        Args:
            uri (str): The full URI for the request.
            payload (dict): The JSON payload to send.

        Returns:
            The JSON response from the server as a dictionary.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(uri, json=payload, timeout=30.0)
            return self._get_response_data(response)

    def _get_response_data(self, response) -> dict:
        response.raise_for_status()

        response_data = response.json()
        logging.info(f"Server responded: {response_data.get('message')}")
        return response_data


client_requester = ClientRequester()
