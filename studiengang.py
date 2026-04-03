# studiengang.py
# Repraesentiert den gesamten Studiengang und bildet die oberste Ebene
# des Fachmodells. Enthaelt die Rahmendaten des Studiums sowie eine
# Liste von Semester-Objekten (Komposition).
# Die Klasse dient ausschliesslich der Datenhaltung - studienweite
# Berechnungen sind im DashboardService ausgelagert.

from datetime import date
from semester import Semester


class Studiengang:

    def __init__(self, name: str, gesamt_ects: int, startdatum: date,
                 ziel_datum: date, ziel_notendurchschnitt: float):
        self.name = name
        self.gesamt_ects = gesamt_ects
        self.startdatum = startdatum
        self.ziel_datum = ziel_datum
        self.ziel_notendurchschnitt = ziel_notendurchschnitt
        # Liste der Semester (Komposition)
        self._semester: list[Semester] = []

    # --- Name ---

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, wert: str):
        if not isinstance(wert, str) or not wert.strip():
            raise ValueError("Studiengangsname darf nicht leer sein.")
        self._name = wert.strip()

    # --- Gesamt-ECTS ---

    @property
    def gesamt_ects(self) -> int:
        return self._gesamt_ects

    @gesamt_ects.setter
    def gesamt_ects(self, wert: int):
        if not isinstance(wert, int) or wert <= 0:
            raise ValueError("Gesamt-ECTS muessen eine positive Ganzzahl sein.")
        self._gesamt_ects = wert

    # --- Startdatum ---

    @property
    def startdatum(self) -> date:
        return self._startdatum

    @startdatum.setter
    def startdatum(self, wert: date):
        if not isinstance(wert, date):
            raise TypeError("Startdatum muss ein date-Objekt sein.")
        self._startdatum = wert

    # --- Zieldatum ---

    @property
    def ziel_datum(self) -> date:
        return self._ziel_datum

    @ziel_datum.setter
    def ziel_datum(self, wert: date):
        if not isinstance(wert, date):
            raise TypeError("Zieldatum muss ein date-Objekt sein.")
        self._ziel_datum = wert

    # --- Ziel-Notendurchschnitt ---

    @property
    def ziel_notendurchschnitt(self) -> float:
        return self._ziel_notendurchschnitt

    @ziel_notendurchschnitt.setter
    def ziel_notendurchschnitt(self, wert: float):
        if not isinstance(wert, (int, float)):
            raise TypeError("Ziel-Notendurchschnitt muss eine Zahl sein.")
        if not 1.0 <= wert <= 4.0:
            raise ValueError("Ziel-Notendurchschnitt muss zwischen 1.0 und 4.0 liegen.")
        self._ziel_notendurchschnitt = float(wert)

    # --- Semester (Komposition) ---

    @property
    def semester(self) -> list[Semester]:
        return self._semester

    def semester_hinzufuegen(self, semester: Semester):
        """Fuegt ein Semester zum Studiengang hinzu."""
        if not isinstance(semester, Semester):
            raise TypeError("Nur Semester-Objekte koennen hinzugefuegt werden.")
        self._semester.append(semester)