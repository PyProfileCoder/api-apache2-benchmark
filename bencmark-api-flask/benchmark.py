import subprocess
import re

def run_benchmark(url: str, requests: int = 1000, concurrency: int = 10):
    # Run Apache Benchmark command
    cmd = f"ab -n {requests} -c {concurrency} {url}"
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Error running benchmark: {result.stderr}")
    
    return parse_benchmark_output(result.stdout)

def parse_benchmark_output(output: str):
    # Use regex to extract relevant metrics from the output
    metrics = {}
    metrics['Requests per second'] = re.search(r"Requests per second:\s+([0-9.]+)", output).group(1)
    metrics['Time per request (ms)'] = re.search(r"Time per request:\s+([0-9.]+)\s\[ms\]", output).group(1)
    metrics['Total transferred (KB)'] = re.search(r"Total transferred:\s+([0-9.]+)\sKB", output).group(1)
    return metrics
