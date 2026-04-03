# pruefungsleistung.py - Klasse Pruefungsleistung mit Note und Abschlussdatum

from datetime import date


class Pruefungsleistung:
    
    """Repraesentiert die Pruefungsleistung eines Moduls.
    
    Attribute:
        note (float): Erzielte Note (1.0 bis 4.0)
        abschlussdatum (date): Datum der Pruefung
    """

    def __init__(self, note: float, abschlussdatum: date):
        # Zuweisung ueber die Setter, damit die Validierung greift
        self.note = note
        self.abschlussdatum = abschlussdatum

    # --- Note ---

    @property
    def note(self) -> float:
        return self._note

    @note.setter
    def note(self, wert: float):
        if not isinstance(wert, (int, float)):
            raise TypeError("Note muss eine Zahl sein.")
        if not 1.0 <= wert <= 4.0:
            raise ValueError("Note muss zwischen 1.0 und 4.0 liegen.")
        self._note = float(wert)

    # --- Abschlussdatum ---

    @property
    def abschlussdatum(self) -> date:
        return self._abschlussdatum

    @abschlussdatum.setter
    def abschlussdatum(self, wert: date):
        if not isinstance(wert, date):
            raise TypeError("Abschlussdatum muss ein date-Objekt sein.")
        self._abschlussdatum = wert