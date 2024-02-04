import requests
from xml.etree import ElementTree as ET
import zipfile
from io import BytesIO
import sqlite3
from datetime import datetime
import logging
import sys

def main():
    # Dynamischer Dateiname für das Log-File
    log_file_path = f"logs/law_reader_run-{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}.txt"

    # Konfiguration des Logging
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # SQLite-Datenbank erstellen und Verbindung herstellen
    conn = sqlite3.connect('gesetze.db')
    cursor = conn.cursor()

    # Tabelle erstellen (falls nicht vorhanden)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gesetze (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jurabk TEXT,
            ausfertigung_datum TEXT,
            zitstelle TEXT,
            periodikum TEXT,
            paragraph TEXT,
            hdline TEXT,
            abschnitt TEXT,
            titel TEXT,
            text TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()

    # Setzen des sys.excepthook
    sys.excepthook = log_exception

    # URL der XML-Datei
    xml_url = "https://www.gesetze-im-internet.de/gii-toc.xml"

    # Zeitmessung starten
    start_time = datetime.now()

    # Herunterladen der XML-Datei 
    try:
        response = requests.get(xml_url)
        response.raise_for_status()  # Fehler auslösen, wenn der HTTP-Statuscode nicht 200 ist

        xml_content = response.content
        root = ET.fromstring(xml_content)

        # Zählvariable für heruntergeladene XML-Dateien initialisieren
        downloaded_xml = 0

        for item in root.findall(".//item"):
            link = item.find("link").text

            zip_response = requests.get(link)
            zip_response.raise_for_status()  # Fehler auslösen, wenn der HTTP-Statuscode nicht 200 ist

            zip_content = BytesIO(zip_response.content)
            process_zip(zip_content, cursor, conn)

            # Inkrementiere die Zählvariable
            downloaded_xml += 1

            # Log hinzufügen
            log_entry = f"ZIP-Datei heruntergeladen und verarbeitet: {link}"
            logging.info(log_entry)
            print(log_entry)
    except requests.exceptions.RequestException as e:
        log_error(f"Fehler beim Herunterladen: {str(e)}")

    # Zeitmessung beenden
    end_time = datetime.now()
    process_time = end_time - start_time

    # Formatierung der Prozesszeit
    process_time_str = str(process_time).split(".")[0]

    # Erfolgsmeldung ins Log schreiben
    success_message = f"Erfolg. {downloaded_xml}. Daten in {process_time_str}."
    logging.info(success_message)
    print(success_message)


def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def process_zip(zip_content, cursor, conn):
    try:
        with zipfile.ZipFile(zip_content, 'r') as zip_ref:
            xml_file_name = zip_ref.namelist()[0]
            xml_content = zip_ref.read(xml_file_name)
            process_xml(xml_content, cursor, conn)
    except Exception as e:
        log_error(e)

def process_xml(xml_content, cursor, conn):
    try:
        root = ET.fromstring(xml_content)

        for norm in root.findall(".//norm"):
            jurabk = norm.find(".//jurabk").text
            ausfertigung_datum_element = norm.find(".//ausfertigung-datum")
            ausfertigung_datum = ausfertigung_datum_element.text if ausfertigung_datum_element is not None else None

            fundstelle_element = norm.find(".//fundstelle/zitstelle")
            zitstelle = fundstelle_element.text if fundstelle_element is not None else None

            periodikum_element = norm.find(".//fundstelle/periodikum")
            periodikum = periodikum_element.text if periodikum_element is not None else None

            enbez_element = norm.find(".//enbez")
            paragraph = enbez_element.text if enbez_element is not None else None

            glbz_element = norm.find(".//gliederungseinheit/gliederungsbez")
            abschnitt = glbz_element.text if glbz_element is not None else None

            titel_element = norm.find(".//gliederungstitel")
            titel = titel_element.text if titel_element is not None else None

            hdline_element = norm.find(".//titel")
            hdline = hdline_element.text if hdline_element is not None else None

            text_element = norm.find(".//textdaten/text/Content/P")
            text = text_element.text if text_element is not None else None

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                INSERT INTO gesetze (jurabk, ausfertigung_datum, zitstelle, periodikum, abschnitt, paragraph, hdline, titel, text, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (jurabk, ausfertigung_datum, zitstelle, periodikum, abschnitt, paragraph, hdline, titel, text, timestamp))

            # Log hinzufügen
            log_entry = f"Eintrag in die Datenbank hinzugefügt: {jurabk} - {abschnitt} - {paragraph}"
            logging.info(log_entry)
            print(log_entry)

        conn.commit()
    except Exception as e:
        log_error(e)

def log_error(error):
    # Fehlermeldung ins Log schreiben
    error_message = f"Fehler: {str(error)}"
    logging.error(error_message)
    print(error_message)


if __name__ == "__main__":
    main()
