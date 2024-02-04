import requests
from xml.etree import ElementTree as ET
import zipfile
from io import BytesIO
import sqlite3
from datetime import datetime

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

def process_zip(zip_content):
    with zipfile.ZipFile(zip_content, 'r') as zip_ref:
        # Annahme: Es gibt genau eine XML-Datei im ZIP-Archiv
        xml_file_name = zip_ref.namelist()[0]
        xml_content = zip_ref.read(xml_file_name)
        process_xml(xml_content)

def process_xml(xml_content):
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

    conn.commit()

# URL der XML-Datei
xml_url = "https://www.gesetze-im-internet.de/gii-toc.xml"

# Herunterladen der XML-Datei
response = requests.get(xml_url)
if response.status_code == 200:
    xml_content = response.content
    root = ET.fromstring(xml_content)

    for item in root.findall(".//item"):
        link = item.find("link").text

        zip_response = requests.get(link)
        if zip_response.status_code == 200:
            zip_content = BytesIO(zip_response.content)
            process_zip(zip_content)
        else:
            print(f"Fehler beim Herunterladen der ZIP-Datei von {link}")
else:
    print(f"Fehler beim Herunterladen der XML-Datei von {xml_url}")
