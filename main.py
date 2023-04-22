from src.main_window import MainWindow
from src.config import Config as cfg


def main():
    app: MainWindow = MainWindow(
        themename=cfg.theme_name, resizable=(False, False)
    )
    app.mainloop()


if __name__ == "__main__":
    main()
