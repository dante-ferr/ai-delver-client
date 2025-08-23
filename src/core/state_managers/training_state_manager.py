from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import customtkinter as ctk
    from src.editor.pages.agent.agent_panel._train_logs_panel import TrainLogsPanel


class TrainingStateManager:
    def __init__(self):
        self._sending_training_request = False
        self._training = False
        self._sending_interrupt_training_request = False

        self.disable_on_train_elements: "set[ctk.CTkBaseClass]" = set()
        self.enable_on_train_elements: "set[ctk.CTkBaseClass]" = set()
        self.train_logs_panel: "TrainLogsPanel | None" = None

        # Defined by the user before training starts, on the episodes slider
        self.amount_of_episodes: int = 0

    def set_train_logs_panel(self, panel: "TrainLogsPanel"):
        self.train_logs_panel = panel
        self._update_ui_state()

    def add_disable_on_train_element(self, element: "ctk.CTkBaseClass"):
        self.disable_on_train_elements.add(element)
        self._update_ui_state()

    def add_enable_on_train_element(self, element: "ctk.CTkBaseClass"):
        self.enable_on_train_elements.add(element)
        self._update_ui_state()

    def update_training_process_log(self, current_episodes: int):
        if self.train_logs_panel:
            self.train_logs_panel.update_training_progress(current_episodes)

    def _update_ui_state(self):
        is_busy = (
            self._sending_training_request
            or self._training
            or self._sending_interrupt_training_request
        )
        is_training_and_not_interrupting = (
            self._training and not self._sending_interrupt_training_request
        )

        state_for_disable_elements = "disabled" if is_busy else "normal"
        for element in self.disable_on_train_elements:
            element.configure(state=state_for_disable_elements)

        state_for_enable_elements = (
            "normal" if is_training_and_not_interrupting else "disabled"
        )
        for element in self.enable_on_train_elements:
            element.configure(state=state_for_enable_elements)

        if self.train_logs_panel:
            if self._sending_training_request:
                self.train_logs_panel.show_log(
                    "sending_request", "Sending training request..."
                )
            else:
                self.train_logs_panel.remove_log("sending_request")

            if self._training:
                self.train_logs_panel.show_training_progress(self.amount_of_episodes)
            else:
                self.train_logs_panel.remove_training_progress()

            if self._sending_interrupt_training_request:
                self.train_logs_panel.show_log(
                    "interrupting", "Interrupting training..."
                )
            else:
                self.train_logs_panel.remove_log("interrupting")

    def reset_states(self):
        self._sending_training_request = False
        self._training = False
        self._sending_interrupt_training_request = False
        self._update_ui_state()

    @property
    def sending_training_request(self):
        return self._sending_training_request

    @sending_training_request.setter
    def sending_training_request(self, value: bool):
        if self._sending_training_request == value:
            return
        self._sending_training_request = value
        self._update_ui_state()

    @property
    def training(self):
        return self._training

    @training.setter
    def training(self, value: bool):
        if self._training == value:
            return
        self._training = value
        self._update_ui_state()

    @property
    def sending_interrupt_training_request(self):
        return self._sending_interrupt_training_request

    @sending_interrupt_training_request.setter
    def sending_interrupt_training_request(self, value: bool):
        if self._sending_interrupt_training_request == value:
            return
        self._sending_interrupt_training_request = value
        self._update_ui_state()


training_state_manager = TrainingStateManager()
