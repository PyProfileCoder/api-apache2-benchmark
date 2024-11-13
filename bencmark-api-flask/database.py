import sqlite3

def init_db():
    conn = sqlite3.connect('benchmark.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS benchmarks (
            id INTEGER PRIMARY KEY,
            api_url TEXT,
            requests_per_sec REAL,
            time_per_request_ms REAL,
            total_transferred_kb REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def store_benchmark(api_url: str, metrics: dict):
    conn = sqlite3.connect('benchmark.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO benchmarks (api_url, requests_per_sec, time_per_request_ms, total_transferred_kb)
        VALUES (?, ?, ?, ?)
    ''', (api_url, metrics['Requests per second'], metrics['Time per request (ms)'], metrics['Total transferred (KB)']))
    conn.commit()
    conn.close()
