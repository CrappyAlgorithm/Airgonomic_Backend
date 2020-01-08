# Airgonomic_Backend

# Einrichtung der Entwicklungsumgebung in VSCode:
- Projekt clonen
- Projektordner in der Konsole öffnen
- Linux: 
```sh
$ python3 -m venv venv
```
- Windows:
```sh
$ python -m venv venv
```
- Projektordner in VSCode öffnen
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
    flask Befehl

# Mögliche Befehle
Befehl | Beschreibung
--- | ---
run | startet das Backend
init-db | legt die Datenbank an bzw bereinigt diese
sample-db | fügt Beispieldaten in die Datenbank ein