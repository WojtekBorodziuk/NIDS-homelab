import sqlite3
from datetime import datetime

DB_NAME = "nids_alerts.db"

def init_db():
    # Tworzymy połączenie i tabelę, jeśli jej nie ma
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source_ip TEXT,
            attack_type TEXT,
            details TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_alert(source_ip, attack_type, details):
    # Zapisujemy nowy incydent do bazy
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO alerts (timestamp, source_ip, attack_type, details)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, source_ip, attack_type, details))
    
    conn.commit()
    conn.close()
