# main.py - Einstiegspunkt der Anwendung

import os
from dashboard_controller import DashboardController
from dashboard_gui import DashboardGUI


def main():
    # JSON-Datei im gleichen Verzeichnis wie main.py
    dateipfad = os.path.join(os.path.dirname(__file__), "daten.json")

    controller = DashboardController(dateipfad)
    gui = DashboardGUI(controller)
    gui.starten()


if __name__ == "__main__":
    main()