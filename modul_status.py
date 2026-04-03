# modul_status.py - Enumeration fuer den Modulstatus

from enum import Enum

class ModulStatus(Enum):

    """Moegliche Zustaende eines Moduls als Aufzaehlungstyp.
    Durch die Verwendung von Enum wird sichergestellt, dass nur
    vordefinierte Werte gesetzt werden koennen.
    """
    
    OFFEN = "Offen"
    IN_BEARBEITUNG = "In Bearbeitung"
    BESTANDEN = "Bestanden"