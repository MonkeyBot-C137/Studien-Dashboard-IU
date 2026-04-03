# modul_status.py
# Enumeration fuer die drei moeglichen Zustaende eines Moduls.
# Durch den Einsatz von Enum wird sichergestellt, dass nur vordefinierte
# Werte verwendet werden - fehleranfaellige Stringvergleiche werden vermieden.

from enum import Enum

class ModulStatus(Enum):
    OFFEN = "Offen"
    IN_BEARBEITUNG = "In Bearbeitung"
    BESTANDEN = "Bestanden"