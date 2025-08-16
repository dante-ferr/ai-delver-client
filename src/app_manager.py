import pyglet
from runtime_view.game import Game
from typing import Optional
import logging
from level_loader import level_loader
from runtime_view.replay import StateSyncReplay
from agent_loader import agent_loader
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from editor import EditorApp


class AppManager:
    def __init__(self):
        self._game = None
        self._replay = None
        self._editor: Optional[EditorApp] = None
        self._is_running = True

    def master_tick(self):
        """
        The main application tick. This is driven by the tkinter event loop
        and is responsible for manually ticking the pyglet clock.
        """
        if not self._is_running:
            return

        # This line tells pyglet to process all pending events and call any
        # functions scheduled with its clock.
        pyglet.clock.tick(poll=True)

        # Reschedule this function to be called again by tkinter's loop.
        # This creates the continuous, non-blocking loop that drives the game.
        if self._editor:
            # We schedule it to run every 1ms. The actual frame rate is
            # still controlled by pyglet's schedule_interval in ViewableRuntime.
            self._editor.after(1, self.master_tick)

    def start_editor(self):
        """
        Starts the editor, which is the master application.
        It will manage the main event loop.
        """
        from editor import EditorApp

        if self._editor is None:
            self._editor = EditorApp()
            logging.info("Starting editor")

            # Handle the editor window closing cleanly
            self._editor.protocol("WM_DELETE_WINDOW", self._on_editor_close)

            # Start the master tick loop, which will drive pyglet.
            self.master_tick()

            # Run the tkinter main loop. This is a blocking call, but our
            # master_tick is now integrated into its event chain.
            self._editor.mainloop()
        else:
            self._editor.deiconify()

    def _on_editor_close(self):
        """Handles the editor window closing, which shuts down everything."""
        logging.info("Editor closing, shutting down application.")
        self._is_running = False  # This will stop the master_tick loop
        self.stop_viewable_runtimes()
        if self._editor:
            self._editor.destroy()

    def _start_runtime(self, runtime_name, runtime_class, *args):
        if getattr(self, f"_{runtime_name}") is not None:
            logging.warning(
                f"{runtime_name.capitalize()} is already running. Stopping first."
            )
            self._stop_runtime(runtime_name)

        if self._editor is not None:
            self._editor.withdraw()

        runtime_instance = runtime_class(*args)
        setattr(self, f"_{runtime_name}", runtime_instance)

        # The runtime will schedule its own update with pyglet's clock.
        runtime_instance.run()

    def _stop_runtime(self, runtime_name):
        runtime_instance = getattr(self, f"_{runtime_name}")
        if runtime_instance is not None:
            runtime_instance.stop()
        setattr(self, f"_{runtime_name}", None)

        # Bring the editor back into view when the game closes.
        if self._editor is not None:
            self._editor.deiconify()
            self._editor.focus_force()

    # The rest of the methods remain the same
    def start_game(self):
        self._start_runtime("game", Game, level_loader.level)

    def stop_game(self):
        self._stop_runtime("game")

    def start_replay(self):
        trajectory = agent_loader.agent.trajectory_loader.trajectory
        if trajectory is None:
            raise RuntimeError("No trajectory loaded")
        self._start_runtime("replay", StateSyncReplay, level_loader.level, trajectory)

    def stop_replay(self):
        self._stop_runtime("replay")

    def stop_viewable_runtimes(self):
        self.stop_game()
        self.stop_replay()

    def stop_editor(self):
        if self._editor is not None:
            self._editor.withdraw()

    @property
    def editor_app(self):
        if self._editor is None:
            raise RuntimeError("Editor app not initialized")
        return self._editor


app_manager = AppManager()
