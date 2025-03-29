import customtkinter as ctk
from typing import Callable
from ..overlay import Overlay


class MessageOverlay(Overlay):
    """
    A warning overlay with a title, a message, and one or more buttons.

    Args:
        message (str): The message to display in the warning overlay.
        button_commands (dict[str, Callable] | None): A dictionary mapping button text to a callable function. If None, only an OK button will be displayed.
    """

    def __init__(
        self,
        message: str,
        subject="Warning",
        button_commands: dict[str, Callable] | None = None,
        paragraphs: list[str] = [],
    ):
        super().__init__(subject)

        text_container = ctk.CTkFrame(self, fg_color="transparent", width=300)
        text_container.pack(pady=4, fill="x", expand=True)

        label = ctk.CTkLabel(text_container, text=message, wraplength=240)
        label.pack(pady=6.4, anchor="w", fill="x")

        for paragraph in paragraphs:
            paragraph_label = ctk.CTkLabel(
                text_container,
                text=paragraph,
                wraplength=240,
            )
            paragraph_label.pack(pady=2, anchor="w", fill="x")

        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.pack(pady=4)

        self._create_buttons(button_commands)

        self._post_init_config()

    def _create_buttons(self, button_commands: dict[str, Callable] | None):
        if button_commands is None:
            buttons = [
                ctk.CTkButton(self.button_container, text="Ok", command=self._close)
            ]
        else:
            buttons = []
            for text, command in button_commands.items():

                def _command_callback(command=command):
                    self._close()
                    command()

                buttons.append(
                    ctk.CTkButton(
                        self.button_container, text=text, command=_command_callback
                    )
                )

        for i, button in enumerate(buttons):
            row = i // 3
            col = i % 3
            button.grid(row=row, column=col, pady=5, padx=5)
