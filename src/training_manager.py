from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import customtkinter as ctk


class TrainingManager:
    def __init__(self):
        self._sending_training_request = False
        self._training = False
        self._sending_interrupt_training_request = False

        self.disable_on_train_elements: "set[ctk.CTkBaseClass]" = set()
        self.enable_on_train_elements: "set[ctk.CTkBaseClass]" = set()
        self.amount_of_episodes = 0  # Amount of train episodes the train will request. It changes according to the user's input on the epsiodes_slider

    def add_disable_on_train_element(self, element: "ctk.CTkBaseClass"):
        self.disable_on_train_elements.add(element)
        self._refresh_training_elements()

    def add_enable_on_train_element(self, element: "ctk.CTkBaseClass"):
        self.enable_on_train_elements.add(element)
        self._refresh_training_elements()

    def _refresh_training_elements(self):
        self.sending_training_request = self.sending_training_request
        self.training = self.training
        self.sending_interrupt_training_request = (
            self.sending_interrupt_training_request
        )

    def reset_states(self):
        self.sending_training_request = False
        self.training = False
        self.sending_interrupt_training_request = False

    @property
    def sending_training_request(self):
        return self._sending_training_request

    @sending_training_request.setter
    def sending_training_request(self, value):
        self._sending_training_request = value

        if value == True:
            for element in self.disable_on_train_elements:
                element.configure(state="disabled")
        else:
            for element in self.disable_on_train_elements:
                element.configure(state="normal")

    @property
    def training(self):
        return self._training

    @training.setter
    def training(self, value):
        self._training = value

        if value == True:
            for element in self.enable_on_train_elements:
                element.configure(state="normal")
            for element in self.disable_on_train_elements:
                element.configure(state="disabled")

    @property
    def sending_interrupt_training_request(self):
        return self._sending_interrupt_training_request

    @sending_interrupt_training_request.setter
    def sending_interrupt_training_request(self, value):
        self._sending_interrupt_training_request = value

        if value == True:
            for element in self.disable_on_train_elements:
                element.configure(state="disabled")
            for element in self.enable_on_train_elements:
                element.configure(state="disabled")
        else:
            for element in self.enable_on_train_elements:
                element.configure(state="disabled")
            for element in self.disable_on_train_elements:
                element.configure(state="normal")


training_manager = TrainingManager()
