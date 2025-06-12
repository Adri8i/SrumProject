

# 🎮 Multiplayer Hangman mit GUI (Python Projekt)

Dies ist ein vollständiges Hangman-Spiel mit Server-Client-Struktur, das mehrere Spieler über das Netzwerk verbindet. Die Spieler können sich über eine grafische Benutzeroberfläche (GUI) verbinden, Buchstaben raten und gemeinsam versuchen, ein verstecktes Wort zu erraten – klassisch wie beim Spiel "Galgenmännchen", inklusive Strichmännchen-Darstellung bei Fehlern.

---

## 📌 Projektübersicht

- **Sprache:** Python 3
- **Art:** Netzwerkspiel (Mehrspieler)
- **Technologien:** `socket`, `threading`, `tkinter`, `csv`
- **Ziel:** Aufbau eines synchronisierten Mehrspieler-Hangman-Spiels mit zentralem Spielzustand

---

## 📁 Projektstruktur

```
hangman-multiplayer/
├── server.py              # Hauptspielserver (verwaltet Spielzustand und Client-Kommunikation)
├── client.py              # GUI-Client (Anzeige und Eingabe für Benutzer)
├── hangman_woerter.csv    # Wortliste (eine Spalte, ein Wort pro Zeile)
├── README.md              # Dokumentation des Projekts
└── screenshots/           # (optional) Screenshots der GUI
```

---

## ⚙️ Voraussetzungen

- **Python 3.8+**
- Benötigte Standardbibliotheken:
  - `socket` – Netzwerkkommunikation
  - `threading` – parallele Verarbeitung von Clients
  - `tkinter` – GUI-Toolkit (standardmäßig enthalten)
  - `csv` – Einlesen der Wortliste
  - `random` – Auswahl eines zufälligen Wortes

---

## 🧑‍🏫 Funktionsweise

### 🔹 Server (`server.py`)
- Lädt Wörter aus einer `.csv`-Datei
- Wählt ein zufälliges Wort als Rätsel
- Verarbeitet Buchstabeneingaben von allen Clients zentral
- Synchronisiert:
  - aktuelles Wort mit Platzhaltern (_ _ _)
  - benutzte Buchstaben
  - verbleibende Fehlversuche
- Schickt Spielstatus nach jedem Zug an **alle Clients**
- Erkennt automatisch Sieg oder Niederlage

### 🔹 Client (`client.py`)
- Stellt Verbindung zum Server her
- Zeigt Spielstand, Feedback und Status
- Eingabe eines Buchstabens über Textfeld
- Zeigt ein grafisches Strichmännchen an, das sich bei Fehlversuchen aufbaut
- GUI reagiert live auf Servernachrichten

---

## 🖥️ Installation & Ausführung

1. **Projekt klonen oder herunterladen**

   ```bash
   git clone https://github.com/Adri8i/SrumProject.git
   cd hangman-multiplayer
   ```

2. **CSV-Datei mit Wörtern vorbereiten**

   Erstelle eine Datei `hangman_woerter.csv` mit einem Wort pro Zeile:

   ```csv
   apfel
   banane
   programm
   python
   ```

3. **Server starten**

   ```bash
   python server.py
   ```

   Ausgabe:
   ```
   Server läuft. Warten auf Verbindungen...
   ```

4. **Clients starten**

   ```bash
   python client.py
   ```

   Du kannst mehrere Clients gleichzeitig starten (auch auf demselben PC, z. B. in mehreren Fenstern), um ein Mehrspielerszenario zu testen.

---

## 🎨 GUI-Features

- **Statusanzeige:** Zeigt das erratene Wort, benutzte Buchstaben, und verbleibende Fehlversuche.
- **Feedbackfeld:** Gibt Rückmeldung nach jeder Eingabe (z. B. "Richtig: a", "Falsch: x").
- **Eingabefeld:** Nur ein Buchstabe pro Zug erlaubt.
- **Strichmännchen-Zeichnung:** Visualisierung der Fehlversuche. Bei 6 Fehlern ist das Spiel verloren.

---

## 🖼️ Beispiel-Screenshot


```text
Wort: _ _ _ _ _ _
Benutzte: a, e, i, o
Versuche: 2

[ Strichmännchen wird gezeichnet ]
```

---

## 🔒 Sicherheit und Threading

- Der Spielserver nutzt `threading.Thread`, um mehrere Clients gleichzeitig zu bedienen.
- Gemeinsamer Zugriff auf globale Variablen wird mit `threading.Lock()` abgesichert (Synchronisation).
- Server aktualisiert zentral den Spielstatus – kein Client hat eine Kopie des Spiels.

---

## 📚 Erweiterungsideen

- Wörter nach Kategorien (z. B. Tiere, Technik)
- Spieleranzahl anzeigen
- Punktesystem oder Highscores
- Spielerneustart nach Gewinn/Verlust
- Web-Version (Flask oder Django)

---

## 📄 Lizenz

Dieses Projekt steht unter der **MIT-Lizenz**. Du darfst es frei verwenden, verändern und verbreiten.
