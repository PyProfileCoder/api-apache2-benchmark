
ab -n 1000 -c 50 http://localhost:5000/
ab -n 500 -c 20 -p post_data.json -T 'application/json' https://pypi.org/project/profiler/


curl -X POST http://127.0.0.1:5000/benchmark -H "Content-Type: application/json" -d '{"api_url": "https://pypi.org/project/profiler/"}'

curl http://127.0.0.1:5000/benchmark/https://pypi.org/project/profiler/


curl -X POST http://127.0.0.1:5000/benchmark/compare -H "Content-Type: application/json" -d '{"api_url": "http://example.com", "timestamp1": "2024-11-13 10:00:00", "timestamp2": "2024-11-13 12:00:00"}'
