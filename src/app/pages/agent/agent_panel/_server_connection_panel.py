import customtkinter as ctk
import asyncio


class ServerConnectionPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.label = ctk.CTkLabel(
            self,
            text="Training server is not connected",
        )
        self.label.pack(pady=(20, 5))

        self.connect_button = ctk.CTkButton(
            self,
            text="Connect now",
            command=lambda: asyncio.run(self._attempt_connection()),
        )
        self.connect_button.pack(pady=(5, 20))

    async def _attempt_connection(self):
        from state_managers import training_state_manager
        from client_requests import client_requester

        training_state_manager.set_value("connected_to_server", "loading")

        await client_requester.initial_request()
