## Airgonomic_Backend

# Einrichtung der Entwicklungsumgebung in VSCode:
- Projekt clonen
- Projektordner in der Konsole öffnen
- Falls nicht vorhanden virtualenv installieren
- Linux: 
```sh
$ python3 -m venv venv
```
- Windows:
```sh
$ python -m venv venv
```
- Projektordner in VSCode öffnen
- Python extension
- Strg+Shift+P "Python: Select Interpreter" auswählen
- Den Interpreter mit der Angabe "venv" auswählen
- Rechtsklick auf den Ordner venv und "Open in Terminal" auswählen
- Linux: 
```sh
$ pip3 install flask
```
- Windows:
```sh
$ pip install flask
```

# Starten der Anwendung:
- In der Konsole ins Hauptverzeichnis des Projekts wechseln
- Setzen von 2 enviroment Variablen
- Linux: 
```sh
$ export FLASK_APP=backend
$ export FLASK_ENV=development
```
- Windows:
```sh
$ set FLASK_APP=backend
$ set FLASK_ENV=development
```
- Nun kann die Anwendung wie folgt genutzt werden
```sh
$ flask <Befehl>
```

# Mögliche Befehle
Befehl | Beschreibung
--- | ---
run | startet das Backend
init-db | legt die Datenbank an bzw bereinigt diese
sample-db | fügt Beispieldaten in die Datenbank ein

# Startparameter für run
Parameter | Beschreibung
--- | ---
-h host-ip :text | Angabe der Socket-IP. Mögliche externe IP's können mit ifconfig eingesehen werden.
-p port :integer | Angabe des Socket-Port.

# Starten der Fenstersteuerung
- In der Konsole in den Ordner control/ wechseln
- Nun kann die Anwendung mit folgendem Befehl gestartet werden:
```sh
$ python3 __init__
```
- Nun schreibt die Anwendung sämtliche Aktivitäten in das Logfile unter control.log.
- Das Programm kann durch die Eingabe von Strg+C beendet werden.
- Beim Beenden werden alle Fenster geschlossen und die aktuelle Configuration gespeichert.
- Um eine erneute Ersteinrichtung zu starten, muss nur die Zeile des Raumes aus der config.txt entfernt werden.
- Zudem kann die Backendadresse in der configurations Datei angepasst werden.