# dashboard_service.py - Studienweite Berechnungen als zustandsloser Service

from datetime import date
from studiengang import Studiengang
from modul_status import ModulStatus


class DashboardService:

    """Buendelt alle studienweiten Berechnungen.
    Die Methoden sind zustandslos - der Studiengang wird jeweils
    als Parameter uebergeben. Dadurch bleibt der Service unabhaengig
    von der Oberflaeche und der Datenstruktur des Fachmodells.
    """

    def berechne_durchschnittsnote(self, studiengang: Studiengang) -> float:
        summe_noten_gewichtet = 0.0
        summe_ects = 0
        for sem in studiengang.semester:
            for modul in sem.module:
                if modul.status == ModulStatus.BESTANDEN and modul.pruefungsleistung:
                    summe_noten_gewichtet += modul.pruefungsleistung.note * modul.ects
                    summe_ects += modul.ects
        if summe_ects == 0:
            return 0.0
        return round(summe_noten_gewichtet / summe_ects, 1)

    def berechne_zeitgewinn(self, studiengang: Studiengang) -> int:
        """Summiert die positiven Effizienz-Werte aller bestandenen Module.
        Positiver Effizienz-Check = Modul schneller als geplant abgeschlossen."""
        tage = 0
        for sem in studiengang.semester:
            for modul in sem.module:
                if modul.status == ModulStatus.BESTANDEN:
                    effizienz = modul.berechne_effizienz_check()
                    if effizienz > 0:
                        tage += effizienz
        return tage

    def berechne_zeitverlust(self, studiengang: Studiengang) -> int:
        """Summiert die negativen Effizienz-Werte aller bestandenen Module.
        Negativer Effizienz-Check = Modul langsamer als geplant abgeschlossen."""
        tage = 0
        for sem in studiengang.semester:
            for modul in sem.module:
                if modul.status == ModulStatus.BESTANDEN:
                    effizienz = modul.berechne_effizienz_check()
                    if effizienz < 0:
                        tage += effizienz
        return tage

    def berechne_gesamtabweichung(self, studiengang: Studiengang) -> int:
        """Netto-Abweichung aus Zeitgewinn und Zeitverlust.
        Positiv = insgesamt schneller als geplant.
        Negativ = insgesamt langsamer als geplant."""
        return self.berechne_zeitgewinn(studiengang) + self.berechne_zeitverlust(studiengang)

    def berechne_zukuenftiger_takt(self, studiengang: Studiengang) -> int:
        """Berechnet wie viele Tage pro 5 ECTS noch noetig sind,
        um das Studium bis zum Zieldatum abzuschliessen.
        Beruecksichtigt auch Module in Bearbeitung, da diese
        bereits Zeit verbrauchen und bald abgeschlossen werden."""
        erreichte_ects = 0
        in_bearbeitung_ects = 0
        for sem in studiengang.semester:
            for modul in sem.module:
                if modul.status == ModulStatus.BESTANDEN:
                    erreichte_ects += modul.ects
                elif modul.status == ModulStatus.IN_BEARBEITUNG:
                    in_bearbeitung_ects += modul.ects

        verbleibende_ects = studiengang.gesamt_ects - erreichte_ects - in_bearbeitung_ects
        if verbleibende_ects <= 0:
            return 0

        verbleibende_tage = (studiengang.ziel_datum - date.today()).days
        if verbleibende_tage <= 0:
            return 0

        return int((verbleibende_tage / verbleibende_ects) * 5)

    def berechne_zeit_bis_studienende(self, studiengang: Studiengang) -> int:
        """Berechnet die verbleibenden Tage bis zum Zieldatum."""
        verbleibende_tage = (studiengang.ziel_datum - date.today()).days
        if verbleibende_tage <= 0:
            return 0
        return verbleibende_tage
    
    def berechne_erreichte_ects(self, studiengang: Studiengang) -> int:
        """Summiert alle ECTS-Punkte von bestandenen Modulen."""
        total = 0
        for sem in studiengang.semester:
            for m in sem.module:
                if m.status == ModulStatus.BESTANDEN:
                    total += m.ects
        return total

    def berechne_durchschnittszeit(self, studiengang: Studiengang) -> int:
        """Berechnet die durchschnittliche Bearbeitungszeit pro Modul in Tagen."""
        gesamt_zeit = 0
        anzahl = 0
        for sem in studiengang.semester:
            for m in sem.module:
                zeit = m.berechne_benoetigte_zeit()
                if zeit > 0:
                    gesamt_zeit += zeit
                    anzahl += 1
        return gesamt_zeit // anzahl if anzahl > 0 else 0