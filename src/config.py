from dataclasses import dataclass


@dataclass
class Config:
    main_window_title: str = "Argus, the eye trainer"
    main_window_width: int = 1020
    main_window_height: int = 632
    theme_name: str = "solar"
    background_squares_size: int = 40
    dot_size: int = 50
    dot_color: int = "red"
    dot_movement_speed: int = 0.10
