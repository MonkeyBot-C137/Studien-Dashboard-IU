# modul_dialog.py - Eingabemaske fuer Moduldaten

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from modul import Modul
from modul_status import ModulStatus


class ModulDialog:

    """Eingabemaske fuer Moduldaten.
    Wird als modales Fenster geoeffnet und kann sowohl fuer das
    Hinzufuegen neuer Module als auch fuer das Bearbeiten
    bestehender Module verwendet werden.
    """

    def __init__(self, parent):
        self._parent = parent
        self._modul = None
        self._ergebnis = False
        self._daten = None

        # Dialog-Fenster erstellen (modal)
        self._dialog = tk.Toplevel(parent)
        self._dialog.title("Modul")
        self._dialog.grab_set()
        self._dialog.resizable(False, False)

        # --- Eingabefelder ---

        # Semester
        tk.Label(self._dialog, text="Semester:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self._semester_var = tk.IntVar(value=1)
        self._semester_dropdown = ttk.Combobox(
            self._dialog,
            textvariable=self._semester_var,
            values=[1, 2, 3, 4, 5, 6],
            state="readonly",
            width=27
        )
        self._semester_dropdown.grid(row=0, column=1, padx=10, pady=5)

        # Name
        tk.Label(self._dialog, text="Kursname:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self._name_entry = tk.Entry(self._dialog, width=30)
        self._name_entry.grid(row=1, column=1, padx=10, pady=5)

        # ECTS
        tk.Label(self._dialog, text="ECTS:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self._ects_entry = tk.Entry(self._dialog, width=30)
        self._ects_entry.grid(row=2, column=1, padx=10, pady=5)

        # Status
        tk.Label(self._dialog, text="Status:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self._status_var = tk.StringVar(value=ModulStatus.OFFEN.value)
        self._status_dropdown = ttk.Combobox(
            self._dialog,
            textvariable=self._status_var,
            values=[s.value for s in ModulStatus],
            state="readonly",
            width=27
        )
        self._status_dropdown.grid(row=3, column=1, padx=10, pady=5)

        # Startdatum
        tk.Label(self._dialog, text="Startdatum (TT.MM.JJJJ):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self._startdatum_entry = tk.Entry(self._dialog, width=30)
        self._startdatum_entry.grid(row=4, column=1, padx=10, pady=5)

        # Note (optional)
        tk.Label(self._dialog, text="Note (optional):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self._note_entry = tk.Entry(self._dialog, width=30)
        self._note_entry.grid(row=5, column=1, padx=10, pady=5)

        # Abschlussdatum (optional)
        tk.Label(self._dialog, text="Abschlussdatum (TT.MM.JJJJ):").grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self._abschlussdatum_entry = tk.Entry(self._dialog, width=30)
        self._abschlussdatum_entry.grid(row=6, column=1, padx=10, pady=5)

        # --- Buttons ---
        button_frame = tk.Frame(self._dialog)
        button_frame.grid(row=7, column=0, columnspan=2, pady=15)

        tk.Button(button_frame, text="Speichern", command=self._speichern).pack(side="left", padx=10)
        tk.Button(button_frame, text="Abbrechen", command=self._abbrechen).pack(side="left", padx=10)

    def set_modul(self, modul: Modul, semester_nummer: int):
        """Befuellt die Eingabefelder mit den Daten eines bestehenden Moduls.
        Wird beim Bearbeiten aufgerufen, nicht beim Hinzufuegen."""
        self._modul = modul
        self._semester_var.set(semester_nummer)
        self._semester_dropdown.config(state="disabled")
        self._name_entry.insert(0, modul.name)
        self._ects_entry.insert(0, str(modul.ects))
        self._status_var.set(modul.status.value)
        if modul.startdatum:
            self._startdatum_entry.insert(0, modul.startdatum.strftime("%d.%m.%Y"))
        if modul.pruefungsleistung:
            self._note_entry.insert(0, str(modul.pruefungsleistung.note))
            self._abschlussdatum_entry.insert(
                0, modul.pruefungsleistung.abschlussdatum.strftime("%d.%m.%Y")
            )

    def _speichern(self):
        """Validiert die Eingaben, speichert die Daten und schliesst den Dialog."""
        daten = self.daten_lesen()
        if daten is not None:
            self._daten = daten
            self._ergebnis = True
            self._dialog.destroy()

    def _abbrechen(self):
        """Schliesst den Dialog ohne zu speichern."""
        self._ergebnis = False
        self._dialog.destroy()

    def anzeigen(self) -> bool:
        """Zeigt den Dialog an und wartet bis er geschlossen wird.
        Gibt True zurueck wenn gespeichert wurde, False bei Abbruch."""
        self._dialog.wait_window()
        return self._ergebnis

    def daten_lesen(self) -> dict:
        """Liest die Eingabefelder aus und gibt sie als Dictionary zurueck.
        Validiert die Eingaben und zeigt bei Fehlern eine Meldung an.
        Gibt None zurueck wenn die Validierung fehlschlaegt."""
        try:
            name = self._name_entry.get().strip()
            if not name:
                raise ValueError("Kursname darf nicht leer sein.")

            try:
                ects = int(self._ects_entry.get())
            except ValueError:
                raise ValueError("ECTS muessen eine Ganzzahl sein.")
            if ects <= 0:
                raise ValueError("ECTS muessen positiv sein.")
            
            # Status-String zurueck in Enum umwandeln
            status = ModulStatus(self._status_var.get())

            # Datum im deutschen Format parsen
            startdatum_text = self._startdatum_entry.get().strip()
            startdatum = self._parse_datum(startdatum_text) if startdatum_text else None

            if startdatum is None and status != ModulStatus.OFFEN:
                raise ValueError("Startdatum ist erforderlich fuer Status 'In Bearbeitung' oder 'Bestanden'.")
            
            if startdatum and startdatum > date.today():
                raise ValueError("Startdatum darf nicht in der Zukunft liegen.")
            
            # Optionale Felder
            note = None
            abschlussdatum = None
            note_text = self._note_entry.get().strip()
            abschluss_text = self._abschlussdatum_entry.get().strip()

            if note_text and abschluss_text:
                note = float(note_text)
                if not 1.0 <= note <= 4.0:
                    raise ValueError("Note muss zwischen 1.0 und 4.0 liegen.")
                abschlussdatum = self._parse_datum(abschluss_text)
                if startdatum is None:
                    raise ValueError("Startdatum ist erforderlich, wenn eine Note eingetragen wird.")
                if abschlussdatum < startdatum:
                    raise ValueError("Abschlussdatum darf nicht vor dem Startdatum liegen.")
                if abschlussdatum > date.today():
                    raise ValueError("Abschlussdatum darf nicht in der Zukunft liegen.")
            elif note_text or abschluss_text:
                raise ValueError("Note und Abschlussdatum muessen beide ausgefuellt sein.")
            
            if note is not None and status != ModulStatus.BESTANDEN:
                raise ValueError("Status muss 'Bestanden' sein, wenn eine Note eingetragen wird.")
            
            if status == ModulStatus.BESTANDEN and note is None:
                raise ValueError("Note und Abschlussdatum sind erforderlich fuer Status 'Bestanden'.")
            

            return {
                "semester_nummer": self._semester_var.get(),
                "name": name,
                "ects": ects,
                "status": status,
                "startdatum": startdatum,
                "note": note,
                "abschlussdatum": abschlussdatum
            }

        except ValueError as e:
            messagebox.showerror("Eingabefehler", str(e), parent=self._dialog)
            return None

    def _parse_datum(self, text: str) -> date:
        """Wandelt einen String im Format TT.MM.JJJJ in ein date-Objekt um."""
        text = text.strip()
        if not text:
            raise ValueError("Datum darf nicht leer sein.")
        try:
            teile = text.split(".")
            return date(int(teile[2]), int(teile[1]), int(teile[0]))
        except (IndexError, ValueError):
            raise ValueError(f"Ungueltiges Datum: '{text}'. Format: TT.MM.JJJJ")