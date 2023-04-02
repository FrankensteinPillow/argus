from dataclasses import dataclass


@dataclass
class Config:
    main_window_title: str = "Argus, the eye trainer"
    main_window_width: int = 1020
    main_window_height: int = 632
