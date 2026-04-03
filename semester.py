# semester.py - Klasse Semester mit zugeordneten Modulen

from modul import Modul


class Semester:
    
    """Repraesentiert ein Semester innerhalb des Studiengangs.
    
    Enthaelt eine Liste von Modul-Objekten (Komposition).
    
    Attribute:
        nummer (int): Semesternummer
        bezeichnung (str): Anzeigename des Semesters
    """

    def __init__(self, nummer: int, bezeichnung: str):
        self.nummer = nummer
        self.bezeichnung = bezeichnung
        # Liste der zugeordneten Module (Komposition)
        self._module: list[Modul] = []

    # --- Nummer ---

    @property
    def nummer(self) -> int:
        return self._nummer

    @nummer.setter
    def nummer(self, wert: int):
        if not isinstance(wert, int) or wert <= 0:
            raise ValueError("Semesternummer muss eine positive Ganzzahl sein.")
        self._nummer = wert

    # --- Bezeichnung ---

    @property
    def bezeichnung(self) -> str:
        return self._bezeichnung

    @bezeichnung.setter
    def bezeichnung(self, wert: str):
        if not isinstance(wert, str) or not wert.strip():
            raise ValueError("Bezeichnung darf nicht leer sein.")
        self._bezeichnung = wert.strip()

    # --- Module (Komposition) ---

    @property
    def module(self) -> list[Modul]:
        return self._module

    def modul_hinzufuegen(self, modul: Modul):
        """Fuegt ein Modul zum Semester hinzu."""
        if not isinstance(modul, Modul):
            raise TypeError("Nur Modul-Objekte koennen hinzugefuegt werden.")
        self._module.append(modul)