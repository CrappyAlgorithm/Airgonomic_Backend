# Airgonomic_Backend

# Einrichtung der Entwicklungsumgebung in VSCode:
- Projekt clonen
- Projektordner in der Konsole öffnen
    Linux: python3 -m venv venv
    Windows: python -m venv venv
- Projektordner in VSCode öffnen
- Strg+Shift+P "Python: Select Interpreter" auswählen
- Den Interpreter mit der Angabe "venv" auswählen
- Rechtsklick auf den Ordner venv und "Open in Terminal" auswählen
    Linux: pip3 install flask
    Windows: pip install flask

# Starten der Anwendung:
- In der Konsole ins Hauptverzeichnis des Projekts wechseln
- Setzen von 2 enviroment Variablen
    Linux: export FLASK_APP=backend
    Linux: export FLASK_ENV=development
    Windows: set FLASK_APP=backend
    Windows: set FLASK_ENV=development
- Nun kann die Anwendung wie folgt genutzt werden
    flask <Befehl>

# Mögliche Befehle
- run: startet das Backend
- init-db: legt die Datenbank an bzw bereinigt diese
- sample-db: fügt Beispieldaten in die Datenbank ein