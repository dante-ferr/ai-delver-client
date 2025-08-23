import customtkinter as ctk
from training_state_manager import training_state_manager
import asyncio
from editor.utils import verify_level_issues
from client_requests import client_requester
import threading


class TrainContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.train_button = ctk.CTkButton(
            self, text="Train", command=self._start_train_thread
        )
        self.train_button.grid(row=0, column=0, padx=(0, 4))

        self.interrupt_training_button = ctk.CTkButton(
            self,
            text="Interrupt Training",
            command=self._start_interrupt_thread,
        )
        self.interrupt_training_button.grid(row=0, column=1, padx=(4, 0))

        self.after(100, self._add_buttons_to_training_manager)

    def _add_buttons_to_training_manager(self):
        training_state_manager.add_disable_on_train_element(self.train_button)
        training_state_manager.add_enable_on_train_element(
            self.interrupt_training_button
        )

    def _start_train_thread(self):
        """
        Starts the training request in a new thread to avoid blocking the GUI.
        """
        thread = threading.Thread(
            target=lambda: asyncio.run(self._train()), daemon=True
        )
        thread.start()

    def _start_interrupt_thread(self):
        """
        Starts the interrupt request in a new thread to avoid blocking the GUI.
        """
        thread = threading.Thread(
            target=lambda: asyncio.run(self._interrupt_training()), daemon=True
        )
        thread.start()

    async def _train(self):
        if not verify_level_issues():
            # This coroutine will now run in a new event loop
            # within a background thread.
            await client_requester.send_training_request()

    async def _interrupt_training(self):
        # This coroutine will also run in a background thread.
        await client_requester.send_interrupt_training_request()
