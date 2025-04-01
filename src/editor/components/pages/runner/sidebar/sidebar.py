import customtkinter as ctk
from level import level_loader
from editor.components.overlay.message_overlay import MessageOverlay


class Sidebar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        play_game_button = ctk.CTkButton(
            self, text="Play Game", command=self._play_game
        )
        play_game_button.pack(pady=8)

    def _play_game(self):
        from app_manager import app_manager

        issues = level_loader.level.issues
        if len(issues) > 0:
            MessageOverlay(f"There are some issues with the level:", paragraphs=issues)
        else:
            app_manager.start_game()
