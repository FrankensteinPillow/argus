import tkinter as tk
from tkinter.ttk import Button

from src.config import Config as cfg


class MainWindow(tk.Tk):
    def __init__(
        self,
        screenName: str | None = None,
        baseName: str | None = None,
        className: str = "Tk",
        useTk: bool = True,
        sync: bool = False,
        use: str | None = None,
    ) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.title(cfg.main_window_title)
        self._set_center_position()
        self._set_start_button()
        self._set_quit_button()

    def _set_center_position(self) -> None:
        w_width: int = cfg.main_window_width
        w_height: int = cfg.main_window_height
        s_width: int = self.winfo_screenwidth()
        s_height: int = self.winfo_screenheight()
        x_shift: int = int(s_width / 2) - int(w_width / 2)
        y_shift: int = int(s_height / 2) - int(w_height / 2)
        self.geometry(f"{w_width}x{w_height}+{x_shift}+{y_shift}")

    def _set_quit_button(self) -> None:
        self._quit_button = Button(
            self, text="Quit", command=self.quit
        )
        self.bind("<Key-Escape>", lambda e: self.quit())
        self._quit_button.pack()

    def _set_start_button(self):
        self._start_button = Button(
            self, text="Start", command=self._start_button_handler
        )
        self._start_button.pack()

    def _start_button_handler(self):
        print("start")
