import customtkinter as ctk
from typing import Callable, Optional


class RangeSliderInput(ctk.CTkFrame):
    """
    A custom widget that combines a slider and an entry field for selecting a numeric value within a range.
    """

    def __init__(
        self,
        master,
        label_text="Value:",
        min_val=0,
        max_val=100,
        init_val=50,
        step=1,
        on_update: Optional[Callable] = None,
        **kwargs,
    ):
        """
        Initialize the RangeSliderInput.

        Args:
            master: The parent widget.
            label_text (str): The text to display above the input.
            min_val (float): The minimum value allowed.
            max_val (float): The maximum value allowed.
            init_val (float): The initial value.
            step (float): The step size for value changes.
            on_update (Callable, optional): A callback function to be called when the value changes.
            **kwargs: Additional keyword arguments for the CTkFrame.
        """
        super().__init__(master, **kwargs)

        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self._on_update = on_update

        # Label and entry
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.pack(anchor="w")

        # Grid configuration
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", expand=True)

        input_frame.grid_columnconfigure(0, weight=0)  # Input (static width)
        input_frame.grid_columnconfigure(1, weight=1)  # Slider (expands)

        # Entry
        self.entry = ctk.CTkEntry(input_frame, width=72)
        self.entry.grid(row=1, column=0, padx=(0, 10), sticky="ew")

        self.entry.bind("<FocusOut>", self._validate_input)
        self.entry.bind("<Return>", self._validate_input)

        # Slider
        self.slider = ctk.CTkSlider(
            input_frame,
            from_=min_val,
            to=max_val,
            number_of_steps=(max_val - min_val) // step,
            command=self._update_from_slider,
        )
        self.slider.grid(row=1, column=1, padx=(0, 10), sticky="ew")

        # Bind scroll events
        self.slider.bind("<MouseWheel>", self._on_mouse_wheel)
        self.slider.bind("<Button-4>", self._on_mouse_wheel)
        self.slider.bind("<Button-5>", self._on_mouse_wheel)

        # Initialize values
        self.slider.set(init_val)
        self._update_entry_text(init_val)

    def _update_from_slider(self, value: float):
        """
        Callback for when the slider value changes. Updates the entry text and triggers the on_update callback.
        """
        if self._on_update:
            self._on_update(value)
        self._update_entry_text(value)

    def _update_entry_text(self, value: float):
        """
        Updates the text in the entry widget to match the current value.
        """
        self.entry.delete(0, "end")
        if isinstance(self.step, int):
            self.entry.insert(0, str(int(value)))
        else:
            self.entry.insert(0, f"{value:.2f}")

    def _validate_input(self, event=None):
        """
        Validates the input in the entry widget when focus is lost or Enter is pressed.
        Clamps the value within the range and snaps it to the step size.

        Args:
            event: The event that triggered validation (optional).
        """
        try:
            val = float(self.entry.get())

            # Clamp value
            if val < self.min_val:
                val = self.min_val
            elif val > self.max_val:
                val = self.max_val

            # Snap to step
            if self.step:
                val = round(val / self.step) * self.step

            self.slider.set(val)
            self._update_entry_text(val)

        except ValueError:
            self._update_entry_text(self.slider.get())

    def _on_mouse_wheel(self, event):
        """
        Handles mouse wheel events to increment or decrement the slider value.
        """
        current_val = self.slider.get()
        if event.num == 5 or event.delta < 0:
            new_val = current_val - self.step
        elif event.num == 4 or event.delta > 0:
            new_val = current_val + self.step
        else:
            return

        if new_val < self.min_val:
            new_val = self.min_val
        elif new_val > self.max_val:
            new_val = self.max_val

        self.slider.set(new_val)
        self._update_from_slider(new_val)

    def get(self):
        """
        Returns the current value of the slider.
        """
        return self.slider.get()

    def set_label(self, text: str):
        """
        Updates the label text.
        """
        self.label.configure(text=text)
