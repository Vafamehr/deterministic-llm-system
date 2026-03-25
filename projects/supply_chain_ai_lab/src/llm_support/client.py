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
                "num_predict": 140,
                "temperature": 0.1,
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
                raw_text = response_data.get("response", "").strip()
                return self._postprocess_response(raw_text)

        except Exception as e:
            return (
                "LLM generation failed. Unable to produce explanation. "
                f"Error: {str(e)}"
            )

    def _postprocess_response(self, text: str) -> str:
        if not text:
            return "LLM returned an empty explanation."

        lines = [line.rstrip() for line in text.splitlines()]
        cleaned_lines = []

        for line in lines:
            if line.strip():
                cleaned_lines.append(line)

        cleaned_text = "\n".join(cleaned_lines).strip()

        marker_positions = []
        for marker in ["SUMMARY", "SCENARIO CHANGES", "RISK TAKEAWAY"]:
            position = cleaned_text.find(marker)
            if position != -1:
                marker_positions.append(position)

        if marker_positions:
            cleaned_text = cleaned_text[min(marker_positions):].strip()

        return cleaned_text