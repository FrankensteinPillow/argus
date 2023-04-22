from dataclasses import dataclass
from src.config import Config as cfg
import tkinter as tk
import ttkbootstrap as ttk
import math
from typing import Callable, Final


@dataclass
class Point:
    """Simple dataclass for the point."""

    x: float
    y: float


def point_diff(p1: Point, p2: Point) -> float:
    """Return eucludian difference between two points."""
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


@dataclass
class MovePrediciton:
    """Class to represent the next point position.

    dx, dy are the pixel difference.
    dp is the parameter difference
    """

    dx: float
    dy: float
    dp: float


Param = float
TrajectoryFunc = Callable[[Param], Point]

STARTING_PARAM_SHIFT: Final = 0.001
RELATIVE_TOLERANCE: Final = 0.01


def predict_move(
    func: TrajectoryFunc,
    param: Param,
    speed: float,
    dt: float
) -> MovePrediciton:
    """Try to predict the param shift to move point with given speed."""
    # calculate the current position
    p0 = func(param)

    # estimate the correct borders for parameter shift
    dp_l = 0
    dp_r = STARTING_PARAM_SHIFT
    while True:
        p1 = func(param + dp_r)
        est_speed = point_diff(p1, p0) / dt
        if est_speed > speed:
            # we discovered a param shift which is far enough
            break

        # else try to double the param shift
        dp_r *= 2.0

    # run binary search for the optimal parameter shift
    while True:
        dp_guess = (dp_l + dp_r) / 2.0
        p1 = func(param + dp_guess)
        est_speed = point_diff(p1, p0) / dt
        if abs(est_speed - speed) <= speed * RELATIVE_TOLERANCE:
            # good approx, return move prediction
            dx = p1.x - p0.x
            dy = p1.y - p0.y
            dp = dp_guess
            return MovePrediciton(dx, dy, dp)

        if est_speed - speed < -speed * RELATIVE_TOLERANCE:
            # point is moving too slow, increase the shift
            dp_l, dp_r = (dp_l + dp_r) / 2.0, dp_r
            continue

        if est_speed - speed > speed * RELATIVE_TOLERANCE:
            # point is moving too fast, decrease the shift
            dp_l, dp_r = dp_l, (dp_l + dp_r) / 2.0
            continue


class MainWindow(ttk.Window):
    def __init__(
        self,
        title="ttkbootstrap",
        themename="litera",
        iconphoto="",
        size=None,
        position=None,
        minsize=None,
        maxsize=None,
        resizable=None,
        hdpi=True,
        scaling=None,
        transient=None,
        overrideredirect=False,
        alpha=1,
    ):
        super().__init__(
            title,
            themename,
            iconphoto,
            size,
            position,
            minsize,
            maxsize,
            resizable,
            hdpi,
            scaling,
            transient,
            overrideredirect,
            alpha,
        )
        self.s_width: int = self.winfo_screenwidth()
        self.s_height: int = self.winfo_screenheight()
        self.is_full_screen: bool = False
        self.set_window_settings()
        self.setup_widgets()
        self.bindings()

    def set_window_settings(self) -> None:
        self.title(cfg.main_window_title)
        self.set_center_position()

    def set_center_position(self) -> None:
        w_width: int = cfg.main_window_width
        w_height: int = cfg.main_window_height
        x_shift: int = int(self.s_width / 2 - w_width / 2)
        y_shift: int = int(self.s_height / 2 - w_height / 2)
        self.geometry(f"{w_width}x{w_height}+{x_shift}+{y_shift}")

    def setup_widgets(self) -> None:
        ...

    def bindings(self) -> None:
        self.bind("<q>", self.q_handler)
        self.bind("<Escape>", self.escape_handler)
        self.bind("<space>", self.space_handler)

    def q_handler(self, _) -> None:
        match self.is_full_screen:
            case True:
                self.return_to_main_screen()
                self.toggle_full_screen()
            case False:
                self.quit()

    def escape_handler(self, _) -> None:
        if self.is_full_screen:
            self.return_to_main_screen()
            self.toggle_full_screen()

    def space_handler(self, e) -> None:
        if not self.is_full_screen:
            self.start()

    def return_to_main_screen(self) -> None:
        self.canvas.pack_forget()
        self.set_window_settings()
        self.setup_widgets()
        self.update()

    def toggle_full_screen(self) -> None:
        self.is_full_screen = not self.is_full_screen
        self.attributes("-fullscreen", self.is_full_screen)

    def start(self):
        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # self.create_background()
        self.create_dot()
        self.toggle_full_screen()

    def create_background(self) -> None:
        for i, x in enumerate(
            range(0, self.s_width + 1, cfg.background_squares_size + 1)
        ):
            for j, y in enumerate(
                range(0, self.s_height + 1, cfg.background_squares_size + 1)
            ):
                color: str = "white" if (j + i) % 2 == 0 else "black"
                self.canvas.create_rectangle(
                    x, y,
                    x+cfg.background_squares_size,
                    y+cfg.background_squares_size,
                    fill=color,
                    width=0
                )

    def create_dot(self) -> None:
        def cardioid(p: Param) -> Point:
            x = 1010 + 200*(1 - math.cos(p)) * math.cos(p)
            y = 810 + 200*(1 - math.cos(p)) * math.sin(p)
            return Point(x=x, y=y)
        def infty(p: Param) -> Point:
            p -= math.pi / 2
            x = 810 + 800 * math.cos(p)
            y = 610 + 600 * math.cos(p) * math.sin(p)
            return Point(x=x, y=y)
        p = infty(0)
        self.dot = self.canvas.create_oval(
            p.x - 10,
            p.y - 10,
            p.x + 10,
            p.y + 10,
            fill=cfg.dot_color,
            width=0
        )
        self.cur_time = 0
        self.p = 0
        self.speed = 18000
        self.dt_ms = 5 #int(1 / 24 * 1000)
        self.func = infty
        self.move()

    def move(self) -> None:
        # def circle(p: Param) -> Point:
        #     return Point(x=410 + math.sin(p) * 400, y=410 + math.cos(p) * 400)

        mp: MovePrediciton = predict_move(
            self.func, self.p, self.speed, self.dt_ms / 1000
        )
        self.canvas.move(self.dot, mp.dx, mp.dy)
        self.p += mp.dp
        dot_pos = self.canvas.coords(self.dot)
        if dot_pos[2] > self.s_width or dot_pos[0] <= 0:
            raise AssertionError(dot_pos)
        if dot_pos[3] > self.s_height or dot_pos[1] <= 0:
            raise AssertionError(dot_pos)
        self.after(self.dt_ms, self.move)


# TODO: Refactoring, разбить виджеты окон на две категории
# 1) Для главного окна
# 2) для окна с тренировкой.
# Упаковывать и убирать эти виджеты в цикле в зависимости от режима
