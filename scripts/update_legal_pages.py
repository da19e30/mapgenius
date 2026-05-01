"""Utility script to generate legal policy pages using the backend LegalAgent endpoint.

It calls the FastAPI endpoint ``/api/v1/legal/generate`` for each policy type and
writes a simple React component that displays the generated text.

Run it after the backend is up (e.g., ``uvicorn app.main:app --port 8000``).
"""
import os
import json
import requests

# Backend URL – adjust if the server runs on a different host/port
BASE_URL = os.getenv("LEGAL_BACKEND_URL", "http://localhost:8000/api/v1")

POLICIES = [
    {"type": "terms", "frontend_path": "frontend/src/pages/Terms.tsx"},
    {"type": "privacy", "frontend_path": "frontend/src/pages/Privacy.tsx"},
    {"type": "cookies", "frontend_path": "frontend/src/pages/Cookies.tsx"},
    {"type": "legal", "frontend_path": "frontend/src/pages/Legal.tsx"},
]


def generate_policy(policy_type: str) -> str:
    payload = {"policy_type": policy_type, "context": {"company_name": "Mapgenius Solutions", "year": "2026"}}
    resp = requests.post(f"{BASE_URL}/legal/generate", json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("content", "")


def write_component(path: str, policy_type: str, content: str):
    # Simple component template – displays the policy text inside a <pre> for formatting
    component = f"""
export default function {policy_type.title()}() {{
  return (
    <div className=\"min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-800 p-8\">
      <div className=\"max-w-4xl mx-auto text-white\">
        <h1 className=\"text-4xl font-extrabold mb-6\">{policy_type.title()}</h1>
        <pre className=\"bg-white/10 p-8 rounded-xl backdrop-blur-sm whitespace-pre-wrap\">{content}</pre>
      </div>
    </div>
  );
}}
"""
    # Ensure the directory exists (it does in repo)
    with open(path, "w", encoding="utf-8") as f:
        f.write(component)
    print(f"Wrote {policy_type} page to {path}")


def main():
    for p in POLICIES:
        text = generate_policy(p["type"])
        write_component(p["frontend_path"], p["type"], text)


if __name__ == "__main__":
    main()
""