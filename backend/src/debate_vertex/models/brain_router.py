import os
import httpx
from ..orchestrator.cue_extractors import estimate_debate_pressure

class HybridBrain:
    def __init__(self):
        # Local points to the K8s Service for vllm
        self.local_endpoint = os.getenv("VLLM_ENDPOINT", "http://vllm-warm:8000/v1/chat/completions")
        self.apex_url = os.getenv("APEX_API_URL", "https://api.groq.com/openai/v1/chat/completions")
        self.apex_key = os.getenv("APEX_API_KEY")
        self.client = httpx.AsyncClient(timeout=45.0)

    async def generate(self, state, prompt: list) -> str:
        # Pressure Check
        is_high_pressure = state.pressure_score > 7.2
        
        if is_high_pressure and self.apex_key:
            return await self._call_apex(prompt)
        
        return await self._call_local(prompt)

    async def _call_local(self, messages: list) -> str:
        try:
            resp = await self.client.post(
                self.local_endpoint,
                json={"model": "Qwen/Qwen2.5-14B-Instruct", "messages": messages, "max_tokens": 512}
            )
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Local Brain Fail: {e}")
            return "My local processes are stalling. One moment."

    async def _call_apex(self, messages: list) -> str:
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024
        }
        headers = {"Authorization": f"Bearer {self.apex_key}"}
        try:
            resp = await self.client.post(self.apex_url, json=payload, headers=headers)
            return resp.json()["choices"][0]["message"]["content"]
        except Exception:
            # Fallback to local if Cloud fails
            return await self._call_local(messages)