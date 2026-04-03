import json
from datetime import date
from studiengang import Studiengang
from semester import Semester
from modul import Modul
from modul_status import ModulStatus
from pruefungsleistung import Pruefungsleistung


class DataManager:
    """Kapselt das Laden und Speichern der Daten in einer JSON-Datei.
    
    Trennt die Dateiverwaltung vollstaendig von der restlichen
    Anwendungslogik. Der Studiengang wird als Parameter uebergeben
    bzw. zurueckgeliefert.
    """

    def __init__(self, dateipfad: str):
        self._dateipfad = dateipfad

    @property
    def dateipfad(self) -> str:
        return self._dateipfad

    def speichern(self, studiengang: Studiengang):
        """Wandelt den gesamten Studiengang in ein Dictionary um
        und speichert es als JSON-Datei. Datumsangaben werden im
        ISO-Format gespeichert, Enums als String-Wert."""
        daten = {
            "name": studiengang.name,
            "gesamt_ects": studiengang.gesamt_ects,
            "startdatum": studiengang.startdatum.isoformat(),
            "ziel_datum": studiengang.ziel_datum.isoformat(),
            "ziel_notendurchschnitt": studiengang.ziel_notendurchschnitt,
            "semester": []
        }
        for sem in studiengang.semester:
            sem_daten = {
                "nummer": sem.nummer,
                "bezeichnung": sem.bezeichnung,
                "module": []
            }
            for modul in sem.module:
                modul_daten = {
                    "name": modul.name,
                    "ects": modul.ects,
                    "status": modul.status.value,
                    "startdatum": modul.startdatum.isoformat() if modul.startdatum else None,
                    "pruefungsleistung": None
                }
                if modul.pruefungsleistung:
                    modul_daten["pruefungsleistung"] = {
                        "note": modul.pruefungsleistung.note,
                        "abschlussdatum": modul.pruefungsleistung.abschlussdatum.isoformat()
                    }
                sem_daten["module"].append(modul_daten)
            daten["semester"].append(sem_daten)

        with open(self._dateipfad, "w") as file:
            json.dump(daten, file, indent=4)

    def laden(self) -> Studiengang:
        """Liest die JSON-Datei und baut daraus den kompletten
        Studiengang mit allen Semestern, Modulen und
        Pruefungsleistungen wieder auf."""
        with open(self._dateipfad, "r") as file:
            daten = json.load(file)

        studiengang = Studiengang(
            name=daten["name"],
            gesamt_ects=daten["gesamt_ects"],
            startdatum=date.fromisoformat(daten["startdatum"]),
            ziel_datum=date.fromisoformat(daten["ziel_datum"]),
            ziel_notendurchschnitt=daten["ziel_notendurchschnitt"]
        )

        for sem_daten in daten["semester"]:
            semester = Semester(
                nummer=sem_daten["nummer"],
                bezeichnung=sem_daten["bezeichnung"]
            )
            for modul_daten in sem_daten["module"]:
                # Status-String zurueck in ModulStatus-Enum umwandeln
                status = ModulStatus(modul_daten["status"])

                pruefungsleistung = None
                if modul_daten["pruefungsleistung"]:
                    pruefungsleistung = Pruefungsleistung(
                        note=modul_daten["pruefungsleistung"]["note"],
                        abschlussdatum=date.fromisoformat(
                            modul_daten["pruefungsleistung"]["abschlussdatum"]
                        )
                    )

                modul = Modul(
                    name=modul_daten["name"],
                    ects=modul_daten["ects"],
                    status=status,
                    startdatum=date.fromisoformat(modul_daten["startdatum"]) if modul_daten["startdatum"] else None,
                    pruefungsleistung=pruefungsleistung
                )
                semester.modul_hinzufuegen(modul)

            studiengang.semester_hinzufuegen(semester)

        return studiengang