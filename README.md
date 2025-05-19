## Bewertungsrechner
### Code-Anforderungen
#### Variablen
- Bezeichner in Englisch
- Trennungen mit Unterstrichen 
- alles kleingeschrieben
#### Zeilen
- maximal 120 Zeichen lang
- maximal 3 Einrückungen
#### Kommentare
- in der Form: `"""..."""`
- Nutzung: Funktion zusammenfassen, spezifisches Erklären
#### Misc.
- Rückgabewert für Funktionen festlegen
- Leerzeichen vor und nach Rechenzeichen, nach Kommata
- inhaltsbasierte Absätze
- eindeutige Commit-Titel

---
### Produktanforderungen
#### Eingabe
- Kurse anlegen (Schülernamen und Benotungssystem)
- Prüfungen anlegen (Punkte pro Aufgabe)
- Ergebnisse eintragen (möglichst mit einem String pro Schüler)
- `csv`-Dateien einlesen
#### Verarbeitung
- Berechnen der Noten (inklusive Plus/Minus in der Sek I)
#### Ausgabe
- Kassenbonausdruck für den Schüler
  - Metadaten (Name, Datum, Kurs, ...)
  - Aufgaben mit Punktzahl und erreichter Punktzahl
  - ggf. Kommentar zur Aufgabe
  - Note und Platz für Unterschrift
- Auswertung für den Lehrer
  - Notenspiegel
  - Notenschnitt
  - weitere Auswertung (beste/schlechteste Aufgabe, Trends, ...)
#### Sonstige
- Berechnungsdauer `< 30 sek`
- Speichern der Daten in `json`-Dateien
- Konfigurierbarkeit (Prozent-Noten-Relation, ...)

