import requests

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3",
    "prompt": "Explain gradient descent in one sentence.",
    "stream": False
}

r = requests.post(url, json=data)

print(r.json()["response"])
