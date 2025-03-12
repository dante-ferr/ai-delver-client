from typing import Callable
import customtkinter as ctk


class LevelToggler:
    def __init__(self):
        self.vars: dict[str, ctk.BooleanVar] = {}

    def add_var(self, var: ctk.BooleanVar, var_name: str):
        self.vars[var_name] = var

    def add_toggle_callback(self, var_name: str, callback: Callable[[bool], None]):
        if var_name not in self.vars:
            raise ValueError(f"No variable named {var_name}.")

        def formatted_callback(*args):
            callback(self.vars[var_name].get())

        self.vars[var_name].trace_add("write", formatted_callback)


# self.var.trace_add("write", self.on_toggle)
