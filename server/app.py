from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from env import EmailEnv

env = EmailEnv()

class Handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Email RL Environment Running")

        elif self.path.startswith("/state"):
            self._set_headers()
            self.wfile.write(json.dumps(env.state()).encode())

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.startswith("/reset"):
            self._set_headers()
            state = env.reset()
            self.wfile.write(json.dumps(state).encode())

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


def main():
    port = 7860
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
