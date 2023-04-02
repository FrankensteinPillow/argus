from src.main_window import MainWindow


def main():
    app: MainWindow = MainWindow(
        screenName="Argus",
        baseName="Argus",
        className="Argus",
    )
    app.mainloop()


if __name__ == "__main__":
    main()
