import tkinter as tk
from tkinter import ttk, messagebox
from dashboard_controller import DashboardController
from modul_dialog import ModulDialog
from modul_status import ModulStatus


class DashboardGUI:
    """Hauptoberflaeche des Dashboards.
    
    Stellt den Studienfortschritt in einer Tabelle dar und zeigt
    aggregierte Kennzahlen an. Kennt den Controller, um Benutzeraktionen
    an ihn zu delegieren. Aktualisiert sich nach jeder Aktion selbst.
    """

    def __init__(self, controller: DashboardController):
        self._controller = controller

        # Hauptfenster erstellen
        self._root = tk.Tk()
        self._root.title("Angewandte Künstliche Intelligenz")
        self._root.minsize(900, 500)

        # --- Buttons oben ---
        button_frame = tk.Frame(self._root)
        button_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(
            button_frame, text="+ Neuen Kurs hinzufuegen",
            command=self._dialog_neues_modul
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="Kurs bearbeiten",
            command=self._dialog_modul_bearbeiten
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="Aktualisieren",
            command=self.aktualisieren
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame, text="Kurs loeschen",
            command=self._modul_loeschen
        ).pack(side="left", padx=5)

        # --- Tabelle ---
        tabellen_frame = tk.Frame(self._root)
        tabellen_frame.pack(fill="both", expand=True, padx=10)
        self._tabelle = ttk.Treeview(
            tabellen_frame,
            columns=("kurs", "status", "zeit", "note", "effizienz"),
            show="tree headings",
            selectmode="browse"
        )

        self._tabelle.heading("#0", text="Semester")
        self._tabelle.heading("kurs", text="Kurs")
        self._tabelle.heading("status", text="Status")
        self._tabelle.heading("zeit", text="Benoetigte Zeit")
        self._tabelle.heading("note", text="Note")
        self._tabelle.heading("effizienz", text="Effizienz-Check")

        self._tabelle.column("#0", width=100)
        self._tabelle.column("kurs", width=300)
        self._tabelle.column("status", width=120, anchor="center")
        self._tabelle.column("zeit", width=110, anchor="center")
        self._tabelle.column("note", width=60, anchor="center")
        self._tabelle.column("effizienz", width=110, anchor="center")

        # Scrollbar fuer die Tabelle
        scrollbar = ttk.Scrollbar(tabellen_frame, orient="vertical", command=self._tabelle.yview)
        self._tabelle.configure(yscrollcommand=scrollbar.set)

        self._tabelle.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Zusammenfassungstabelle ---
        zusammenfassung_frame = tk.Frame(self._root)
        zusammenfassung_frame.pack(fill="x", padx=10)

        self._zusammenfassung = ttk.Treeview(
            zusammenfassung_frame,
            columns=("kurs", "status", "zeit", "note", "effizienz"),
            show="",
            height=1,
            selectmode="none"
        )

        self._zusammenfassung.column("#0", width=100)
        self._zusammenfassung.column("kurs", width=300)
        self._zusammenfassung.column("status", width=221, anchor="center")
        self._zusammenfassung.column("zeit", width=100, anchor="center")
        self._zusammenfassung.column("note", width=60, anchor="center")
        self._zusammenfassung.column("effizienz", width=110, anchor="center")

        self._zusammenfassung.tag_configure("zusammenfassung", font=("Arial", 10, "bold"))
        self._zusammenfassung.pack(fill="x")

        # --- Kennzahlen unten ---
        self._kennzahlen_frame = tk.Frame(self._root)
        self._kennzahlen_frame.pack(fill="x", padx=10, pady=10)

        # Linke Seite: ECTS, Zeit, Durchschnitt
        links = tk.Frame(self._kennzahlen_frame)
        links.pack(side="left", padx=20)

        self._label_durchschnitt = tk.Label(links, text="", font=("Arial", 10))
        self._label_durchschnitt.pack(anchor="w")

        # Rechte Seite: Zeitkennzahlen
        rechts = tk.Frame(self._kennzahlen_frame)
        rechts.pack(side="right", padx=20)

        self._label_zeitgewinn = tk.Label(rechts, text="", font=("Arial", 10))
        self._label_zeitgewinn.pack(anchor="w")

        self._label_zeitverlust = tk.Label(rechts, text="", font=("Arial", 10))
        self._label_zeitverlust.pack(anchor="w")

        self._label_gesamtabweichung = tk.Label(rechts, text="", font=("Arial", 10))
        self._label_gesamtabweichung.pack(anchor="w")

        self._label_takt = tk.Label(rechts, text="", font=("Arial", 10))
        self._label_takt.pack(anchor="w")

        self._label_restzeit = tk.Label(rechts, text="", font=("Arial", 10))
        self._label_restzeit.pack(anchor="w")

        # Daten laden und anzeigen
        self.aktualisieren()

    def starten(self):
        """Startet die Anwendung (Hauptschleife von tkinter)."""
        self._root.mainloop()

    def aktualisieren(self):
        """Aktualisiert die Tabelle und alle Kennzahlen.
        Wird nach jeder Aktion von der GUI selbst aufgerufen."""
        self._tabelle_aktualisieren()
        self._zusammenfassung_aktualisieren()
        self._kennzahlen_aktualisieren()

    def _tabelle_aktualisieren(self):
        """Loescht die Tabelle und befuellt sie neu mit allen Modulen,
        gruppiert nach Semestern."""
        for item in self._tabelle.get_children():
            self._tabelle.delete(item)

        sg = self._controller.studiengang
        for sem in sg.semester:
            # Semester als Gruppen-Knoten einfuegen
            sem_id = self._tabelle.insert("", "end", text=sem.bezeichnung, open=True)

            for modul in sem.module:
                zeit = ""
                note = ""
                effizienz = ""

                if modul.status == ModulStatus.BESTANDEN and modul.pruefungsleistung:
                    zeit = f"{modul.berechne_benoetigte_zeit()} Tage"
                    note = str(modul.pruefungsleistung.note)
                    tage = modul.berechne_effizienz_check()
                    vorzeichen = "+" if tage > 0 else ""
                    effizienz = f"{vorzeichen}{tage} Tage"
                elif modul.status == ModulStatus.IN_BEARBEITUNG and modul.startdatum:
                    zeit = f"{modul.berechne_benoetigte_zeit()} Tage"

                # Modul als Kind des Semesters einfuegen
                self._tabelle.insert(sem_id, "end", text="", values=(
                    modul.name,
                    modul.status.value,
                    zeit,
                    note,
                    effizienz
                ))

    def _zusammenfassung_aktualisieren(self):
        """Aktualisiert die Zusammenfassungstabelle durch Abruf der Service-Logik."""
        for item in self._zusammenfassung.get_children():
            self._zusammenfassung.delete(item)

        sg = self._controller.studiengang
        service = self._controller.service

        erreichte_ects = service.berechne_erreichte_ects(sg)
        d_zeit = service.berechne_durchschnittszeit(sg)
        durchschnitt_zeit_text = f"Ø {d_zeit} Tage" if d_zeit > 0 else ""

        durchschnitt_note = service.berechne_durchschnittsnote(sg)
        durchschnitt_note_text = f"Ø {durchschnitt_note}" if durchschnitt_note > 0 else ""

        self._zusammenfassung.insert("", "end", text="", values=(
            f"{erreichte_ects} von {sg.gesamt_ects} ECTS",
            "",
            durchschnitt_zeit_text,
            durchschnitt_note_text,
            ""
        ), tags=("zusammenfassung",))
        

    def _kennzahlen_aktualisieren(self):
        """Berechnet und zeigt die aggregierten Kennzahlen an."""
        sg = self._controller.studiengang
        service = self._controller.service

        # Erreichte ECTS erneut unabhaengig zaehlen
        erreichte_ects = 0
        for sem in sg.semester:
            for modul in sem.module:
                if modul.status == ModulStatus.BESTANDEN:
                    erreichte_ects += modul.ects

        # Durchschnittsnote
        durchschnitt = service.berechne_durchschnittsnote(sg)
        farbe = "green" if durchschnitt <= sg.ziel_notendurchschnitt and durchschnitt > 0 else "red"
        if durchschnitt == 0:
            farbe = "black"
        self._label_durchschnitt.config(
            text=f"Notendurchschnitt: {durchschnitt} (Ziel: {sg.ziel_notendurchschnitt})",
            fg=farbe
        )

        # Zeitgewinn
        zeitgewinn = service.berechne_zeitgewinn(sg)
        self._label_zeitgewinn.config(
            text=f"Zeitgewinn: {zeitgewinn} Tage",
            fg="green" if zeitgewinn > 0 else "black"
        )

        # Zeitverlust
        zeitverlust = service.berechne_zeitverlust(sg)
        self._label_zeitverlust.config(
            text=f"Zeitverlust: {zeitverlust} Tage",
            fg="red" if zeitverlust < 0 else "black"
        )

        # Gesamtabweichung
        abweichung = service.berechne_gesamtabweichung(sg)
        farbe = "green" if abweichung >= 0 else "red"
        self._label_gesamtabweichung.config(
            text=f"Gesamtabweichung: {abweichung} Tage",
            fg=farbe
        )

        # Zukuenftiger Takt
        takt = service.berechne_zukuenftiger_takt(sg)
        self._label_takt.config(text=f"Zukuenftiger Takt: {takt} Tage / 5 ECTS")

        # Zeit bis Studienende
        rest_tage = service.berechne_zeit_bis_studienende(sg)
        jahre = rest_tage // 365
        rest = rest_tage % 365
        wochen = rest // 7
        tage = rest % 7
        self._label_restzeit.config(
            text=f"Zeit bis Studienende: {jahre} Jahre {wochen} Wochen {tage} Tage"
        )

    # --- Dialoge ---

    def _dialog_neues_modul(self):
        """Oeffnet den Dialog zum Hinzufuegen eines neuen Moduls."""
        dialog = ModulDialog(self._root)
        if dialog.anzeigen():
            daten = dialog._daten
            if daten:
                try:
                    self._controller.modul_hinzufuegen(
                        semester_nummer=daten["semester_nummer"],
                        name=daten["name"],
                        ects=daten["ects"],
                        status=daten["status"],
                        startdatum=daten["startdatum"],
                        note=daten["note"],
                        abschlussdatum=daten["abschlussdatum"]
                    )
                except ValueError as e:
                    messagebox.showerror("Fehler", str(e), parent=self._root)
                self.aktualisieren()

    def _dialog_modul_bearbeiten(self):
        """Oeffnet den Dialog zum Bearbeiten des ausgewaehlten Moduls."""
        auswahl = self._tabelle.selection()
        if not auswahl:
            messagebox.showinfo("Hinweis", "Bitte waehle zuerst ein Modul aus.", parent=self._root)
            return

        item = auswahl[0]
        werte = self._tabelle.item(item)["values"]

        # Pruefen ob ein Modul oder ein Semester ausgewaehlt ist
        if not werte:
            messagebox.showinfo("Hinweis", "Bitte waehle ein Modul aus, kein Semester.", parent=self._root)
            return

        modul_name = werte[0]

        # Semester ueber den Parent-Knoten finden
        parent_id = self._tabelle.parent(item)
        semester_bez = self._tabelle.item(parent_id)["text"]

        modul = None
        semester_nummer = None
        for sem in self._controller.studiengang.semester:
            if sem.bezeichnung == semester_bez:
                semester_nummer = sem.nummer
                for m in sem.module:
                    if m.name == modul_name:
                        modul = m
                        break
                break

        if modul is None:
            return

        dialog = ModulDialog(self._root)
        dialog.set_modul(modul, semester_nummer)
        if dialog.anzeigen():
            daten = dialog._daten
            if daten:
                self._controller.modul_bearbeiten(
                    modul=modul,
                    name=daten["name"],
                    ects=daten["ects"],
                    status=daten["status"],
                    startdatum=daten["startdatum"],
                    note=daten["note"],
                    abschlussdatum=daten["abschlussdatum"]
                )
                self.aktualisieren()

    def _modul_loeschen(self):
        """Loescht das ausgewaehlte Modul nach Bestaetigung."""
        auswahl = self._tabelle.selection()
        if not auswahl:
            messagebox.showinfo("Hinweis", "Bitte waehle zuerst ein Modul aus.", parent=self._root)
            return

        item = auswahl[0]
        werte = self._tabelle.item(item)["values"]

        if not werte:
            messagebox.showinfo("Hinweis", "Bitte waehle ein Modul aus, kein Semester.", parent=self._root)
            return

        modul_name = werte[0]
        parent_id = self._tabelle.parent(item)
        semester_bez = self._tabelle.item(parent_id)["text"]

        antwort = messagebox.askyesno(
            "Modul loeschen",
            f"Modul '{modul_name}' wirklich loeschen?",
            parent=self._root
        )

        if antwort:
            for sem in self._controller.studiengang.semester:
                if sem.bezeichnung == semester_bez:
                    self._controller.modul_loeschen(sem.nummer, modul_name)
                    break
            self.aktualisieren()