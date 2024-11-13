from flask import Flask, request, jsonify
from datetime import datetime
from benchmark import run_benchmark
from database import store_benchmark
import sqlite3

app = Flask(__name__)

# Endpoint to run a new benchmark and store the results
@app.route('/benchmark', methods=['POST'])
def benchmark():
    data = request.json
    api_url = data['api_url']
    requests = data.get('requests', 1000)
    concurrency = data.get('concurrency', 10)

    try:
        metrics = run_benchmark(api_url, requests, concurrency)
        store_benchmark(api_url, metrics)
        return jsonify({"message": "Benchmark completed", "metrics": metrics}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to get the benchmark results for a specific API
@app.route('/benchmark/<api_url>', methods=['GET'])
def get_benchmark(api_url):
    conn = sqlite3.connect('benchmark.db')
    c = conn.cursor()
    c.execute("SELECT * FROM benchmarks WHERE api_url = ? ORDER BY timestamp DESC", (api_url,))
    results = c.fetchall()
    conn.close()

    benchmarks = [{
        "id": row[0],
        "api_url": row[1],
        "requests_per_sec": row[2],
        "time_per_request_ms": row[3],
        "total_transferred_kb": row[4],
        "timestamp": row[5]
    } for row in results]

    return jsonify(benchmarks)

# Endpoint to compare two benchmark results
@app.route('/benchmark/compare', methods=['POST'])
def compare_benchmarks():
    data = request.json
    api_url = data['api_url']
    timestamp1 = data['timestamp1']
    timestamp2 = data['timestamp2']

    conn = sqlite3.connect('benchmark.db')
    c = conn.cursor()
    c.execute("SELECT * FROM benchmarks WHERE api_url = ? AND timestamp = ?", (api_url, timestamp1))
    result1 = c.fetchone()

    c.execute("SELECT * FROM benchmarks WHERE api_url = ? AND timestamp = ?", (api_url, timestamp2))
    result2 = c.fetchone()

    conn.close()

    if result1 and result2:
        comparison = {
            "api_url": api_url,
            "benchmark_1": {
                "timestamp": result1[5],
                "requests_per_sec": result1[2],
                "time_per_request_ms": result1[3],
                "total_transferred_kb": result1[4]
            },
            "benchmark_2": {
                "timestamp": result2[5],
                "requests_per_sec": result2[2],
                "time_per_request_ms": result2[3],
                "total_transferred_kb": result2[4]
            },
            "comparison": {
                "requests_per_sec_diff": float(result2[2]) - float(result1[2]),
                "time_per_request_ms_diff": float(result2[3]) - float(result1[3]),
                "total_transferred_kb_diff": float(result2[4]) - float(result1[4])
            }
        }
        return jsonify(comparison)
    else:
        return jsonify({"error": "Benchmark results not found for one or both timestamps"}), 404
