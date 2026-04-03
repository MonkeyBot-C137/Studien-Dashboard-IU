# modul.py - Klasse Modul mit Stammdaten und modulbezogenen Berechnungen

from datetime import date
from modul_status import ModulStatus
from pruefungsleistung import Pruefungsleistung


# Planungsgrundlage: 5 ECTS entsprechen 30 Tagen Bearbeitungszeit
TAGE_PRO_5_ECTS = 30


class Modul:
    
    """Repraesentiert ein einzelnes Modul im Studiengang.
    Attribute:
        name (str): Kursname des Moduls
        ects (int): ECTS-Punkte des Moduls
        status (ModulStatus): Aktueller Bearbeitungsstatus
        startdatum (date): Beginn der Bearbeitung (None wenn Status OFFEN)
        pruefungsleistung (Pruefungsleistung): Ergebnis der Pruefung (None wenn noch nicht bestanden)
    """
    def __init__(self, name: str, ects: int, status: ModulStatus,
                 startdatum: date, pruefungsleistung: Pruefungsleistung = None):
        self.name = name
        self.ects = ects
        self.status = status
        self.startdatum = startdatum
        self.pruefungsleistung = pruefungsleistung

    # --- Name ---

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, wert: str):
        if not isinstance(wert, str) or not wert.strip():
            raise ValueError("Modulname darf nicht leer sein.")
        self._name = wert.strip()

    # --- ECTS ---

    @property
    def ects(self) -> int:
        return self._ects

    @ects.setter
    def ects(self, wert: int):
        if not isinstance(wert, int) or wert <= 0:
            raise ValueError("ECTS muessen eine positive Ganzzahl sein.")
        self._ects = wert

    # --- Status ---

    @property
    def status(self) -> ModulStatus:
        return self._status

    @status.setter
    def status(self, wert: ModulStatus):
        if not isinstance(wert, ModulStatus):
            raise TypeError("Status muss ein ModulStatus-Wert sein.")
        self._status = wert

    # --- Startdatum ---

    @property
    def startdatum(self) -> date:
        return self._startdatum

    @startdatum.setter
    def startdatum(self, wert: date):
        if wert is not None and not isinstance(wert, date):
            raise TypeError("Startdatum muss ein date-Objekt oder None sein.")
        self._startdatum = wert

    # --- Pruefungsleistung (optional, Komposition 0..1) ---

    @property
    def pruefungsleistung(self) -> Pruefungsleistung:
        return self._pruefungsleistung

    @pruefungsleistung.setter
    def pruefungsleistung(self, wert: Pruefungsleistung):
        if wert is not None and not isinstance(wert, Pruefungsleistung):
            raise TypeError("Muss eine Pruefungsleistung oder None sein.")
        self._pruefungsleistung = wert

    # --- Berechnungen ---

    def berechne_benoetigte_zeit(self) -> int:
        """Berechnet die Bearbeitungszeit in Tagen.
        Bei bestandenen Modulen: Tage zwischen Start und Abschluss.
        Bei Modulen in Bearbeitung: Tage seit Startdatum bis heute."""
        if self._startdatum is None:
            return 0
        if self._pruefungsleistung is not None:
            differenz = self._pruefungsleistung.abschlussdatum - self._startdatum
            return differenz.days
        if self._status == ModulStatus.IN_BEARBEITUNG:
            return (date.today() - self._startdatum).days
        return 0

    def berechne_effizienz_check(self) -> int:
        """Berechnet die Abweichung zwischen Soll- und Ist-Zeit in Tagen.
        Positiver Wert = schneller als geplant (Zeitgewinn).
        Negativer Wert = langsamer als geplant (Zeitverlust).
        Sollzeit: 5 ECTS entsprechen 30 Tagen."""
        if self._pruefungsleistung is None:
            return 0
        sollzeit = (self._ects / 5) * TAGE_PRO_5_ECTS
        istzeit = self.berechne_benoetigte_zeit()
        return int(sollzeit - istzeit)