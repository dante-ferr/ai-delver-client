import customtkinter as ctk
from typing import Literal, Callable
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
    ):
        super().__init__(subject)

        self.geometry("300x150")

        label = ctk.CTkLabel(
            self, text=message, corner_radius=10, width=280, height=100, wraplength=240
        )
        label.pack(pady=4)

        button_container = ctk.CTkFrame(self, fg_color="transparent")
        button_container.pack(pady=4)

        if button_commands is None:
            buttons = [ctk.CTkButton(button_container, text="Ok", command=self._close)]
        else:
            buttons = []
            for text, command in button_commands.items():

                def _command_callback(command=command):
                    self._close()
                    command()

                buttons.append(
                    ctk.CTkButton(
                        button_container, text=text, command=_command_callback
                    )
                )

        for i, button in enumerate(buttons):
            row = i // 3
            col = i % 3
            button.grid(row=row, column=col, pady=5, padx=5)

        self.after(10, self.grab_set)
