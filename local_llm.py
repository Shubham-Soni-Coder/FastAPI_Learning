import requests
import json

URL = "http://192.168.1.8:11434/api/generate"

payload = {
    "model": "llama3.2:1b",
    "prompt": "Write a Python function to check prime number",
    "stream": True,
}

r = requests.post(URL, json=payload, stream=True)

for line in r.iter_lines():
    if line:
        data = json.loads(line.decode())
        if "response" in data:
            print(data["response"], end="", flush=True)
