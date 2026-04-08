import os
import json
from env import EmailEnv
from http.server import BaseHTTPRequestHandler, HTTPServer

# OPTIONAL: OpenAI client
try:
    from openai import OpenAI
    client = OpenAI(base_url=os.getenv("API_BASE_URL"))
    MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")
    USE_LLM = True
except:
    USE_LLM = False

env = EmailEnv()

print("[START]")

def llm_agent(email):
    prompt = f"""
    Classify this email into one of: spam, important, normal.
    Email: {email}
    Answer only one word.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().lower()


def smart_agent(email):
    email = email.lower()
    if "win" in email or "free" in email:
        return "spam"
    elif "meeting" in email or "deadline" in email:
        return "important"
    else:
        return "normal"


# RUN BASELINE (IMPORTANT FOR LOGS)
state = env.reset()
done = False
total_reward = 0
steps = 0

while not done:
    print("[STEP]", state)

    if USE_LLM:
        action = llm_agent(state["email"])
    else:
        action = smart_agent(state["email"])

    state, reward, done, _ = env.step(action)

    total_reward += reward
    steps += 1

    print("Action:", action)
    print("Reward:", reward)

score = max(0, min(1, total_reward / steps))

print("[END]")
print("Final Score:", score)


# 🔥 OPENENV API SERVER (FINAL FIXED)
class Handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        # ✅ HANDLE ROOT + QUERY PARAMS (/ or /?anything)
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Email RL Environment Running")

        # ✅ STATE ENDPOINT (also supports query params)
        elif self.path.startswith("/state"):
            self._set_headers()
            self.wfile.write(json.dumps(env.state()).encode())

        else:
            self.send_error(404)

    def do_POST(self):
        # ✅ RESET ENDPOINT
        if self.path.startswith("/reset"):
            self._set_headers()
            state = env.reset()
            self.wfile.write(json.dumps(state).encode())

        # ✅ STEP ENDPOINT
        elif self.path.startswith("/step"):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)

            action = data.get("action", "normal")

            state, reward, done, _ = env.step(action)

            response = {
                "state": state,
                "reward": reward,
                "done": done
            }

            self._set_headers()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_error(404)


port = 7860
server = HTTPServer(("0.0.0.0", port), Handler)

print(f"Server running on port {port}")
server.serve_forever()
