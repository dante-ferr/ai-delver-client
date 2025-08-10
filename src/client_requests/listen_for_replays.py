import websockets
import logging
import dill
import base64
import binascii


async def listen_for_replays(uri="ws://localhost:8001/replay"):
    """
    Connects to a WebSocket and yields received replay frames.

    This function is an async generator, which means it can be used
    in an 'async for' loop to process messages as they arrive.

    Args:
        uri (str): The WebSocket URI to connect to.

    Yields:
        The deserialized replay frame received from the server.

    Raises:
        Exception: Propagates exceptions from the WebSocket connection or message decoding.
    """
    logging.info(f"Connecting to WebSocket at {uri} to receive replay data...")
    try:
        # The 'async with' ensures the connection is properly closed
        async with websockets.connect(uri) as websocket:
            logging.info(
                "WebSocket connection established. Waiting for replay frames..."
            )

            # This loop waits for messages and yields them one by one
            async for message in websocket:
                yield message

    except websockets.exceptions.ConnectionClosed as e:
        logging.warning(f"WebSocket connection closed: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred in WebSocket listener: {e}")
        # Re-raise the exception to be handled by the caller
        raise
