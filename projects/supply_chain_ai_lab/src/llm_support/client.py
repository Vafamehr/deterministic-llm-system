from __future__ import annotations

import json
import urllib.request


class LLMClient:
    def __init__(
        self,
        model_name: str = "llama3",
        base_url: str = "http://localhost:11434/api/generate",
        timeout: int = 120,
    ) -> None:
        self.model_name = model_name
        self.base_url = base_url
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 180,
                "temperature": 0.3,
            },
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            self.base_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                response_data = json.loads(response.read().decode("utf-8"))
                return response_data.get("response", "").strip()

        except Exception as e:
            return (
                "LLM generation failed. Unable to produce explanation. "
                f"Error: {str(e)}"
            )