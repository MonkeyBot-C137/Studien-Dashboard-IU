import os
from datetime import date
from studiengang import Studiengang
from semester import Semester
from modul import Modul
from modul_status import ModulStatus
from pruefungsleistung import Pruefungsleistung
from dashboard_service import DashboardService
from data_manager import DataManager


class DashboardController:

    """Zentrale Steuerung der Anwendung.
    
    Koordiniert die Ablaeufe zwischen Fachmodell, Service und DataManager.
    Der Controller kennt die GUI nicht - die Aktualisierung der Darstellung
    wird von der GUI selbst angestossen.
    """

    def __init__(self, dateipfad: str):
        self._service = DashboardService()
        self._data_manager = DataManager(dateipfad)
        self._studiengang = None
        self.daten_laden()

    # --- Zugriff auf den Studiengang ---

    @property
    def studiengang(self) -> Studiengang:
        return self._studiengang

    @property
    def service(self) -> DashboardService:
        return self._service

    # --- Daten laden und speichern ---

    def daten_laden(self):
        """Laedt den Studiengang aus der JSON-Datei.
        Falls keine Datei existiert, wird ein neuer Studiengang
        mit Standardwerten und leeren Semestern angelegt."""
        if os.path.exists(self._data_manager.dateipfad):
            self._studiengang = self._data_manager.laden()
        else:
            self._studiengang = Studiengang(
                name="Angewandte Kuenstliche Intelligenz",
                gesamt_ects=180,
                startdatum=date(2024, 10, 1),
                ziel_datum=date(2028, 7, 31),
                ziel_notendurchschnitt=2.0
            )
            # Sechs Semester anlegen (Regelstudienzeit)
            for i in range(1, 7):
                sem = Semester(nummer=i, bezeichnung=f"{i}. Semester")
                self._studiengang.semester_hinzufuegen(sem)
            self.daten_speichern()

    def daten_speichern(self):
        """Speichert den aktuellen Studiengang in der JSON-Datei."""
        self._data_manager.speichern(self._studiengang)

    # --- Modul hinzufuegen ---

    def modul_hinzufuegen(self, semester_nummer: int, name: str, ects: int,
                          status: ModulStatus, startdatum: date,
                          note: float = None, abschlussdatum: date = None):
        """Erstellt ein neues Modul und fuegt es dem angegebenen Semester hinzu.
        Falls eine Note und ein Abschlussdatum uebergeben werden,
        wird automatisch eine Pruefungsleistung erstellt."""
        pruefungsleistung = None
        if note is not None and abschlussdatum is not None:
            pruefungsleistung = Pruefungsleistung(note=note, abschlussdatum=abschlussdatum)

        modul = Modul(
            name=name,
            ects=ects,
            status=status,
            startdatum=startdatum,
            pruefungsleistung=pruefungsleistung
        )

        # Pruefen ob ein Modul mit gleichem Namen im Semester bereits existiert + Modul hinzufuegen
        for sem in self._studiengang.semester:
            if sem.nummer == semester_nummer:
                for m in sem.module:
                    if m.name.lower() == name.lower():
                        raise ValueError(f"Ein Modul mit dem Namen '{name}' existiert bereits in diesem Semester.")
                sem.modul_hinzufuegen(modul)
                break

        self.daten_speichern()

    # --- Modul bearbeiten ---

    def modul_bearbeiten(self, modul: Modul, name: str, ects: int,
                         status: ModulStatus, startdatum: date,
                         note: float = None, abschlussdatum: date = None):
        """Aktualisiert ein bestehendes Modul mit neuen Werten.
        Falls eine Note und ein Abschlussdatum uebergeben werden,
        wird die Pruefungsleistung erstellt oder aktualisiert.
        Falls beides None ist, wird eine vorhandene Pruefungsleistung entfernt."""
        modul.name = name
        modul.ects = ects
        modul.status = status
        modul.startdatum = startdatum

        if note is not None and abschlussdatum is not None:
            modul.pruefungsleistung = Pruefungsleistung(
                note=note, abschlussdatum=abschlussdatum
            )
        else:
            modul.pruefungsleistung = None

        self.daten_speichern()

    # --- Modul loeschen ---

    def modul_loeschen(self, semester_nummer: int, modul_name: str):
        """Loescht ein Modul aus dem angegebenen Semester."""
        for sem in self._studiengang.semester:
            if sem.nummer == semester_nummer:
                for modul in sem.module:
                    if modul.name == modul_name:
                        sem.module.remove(modul)
                        self.daten_speichern()
                        return