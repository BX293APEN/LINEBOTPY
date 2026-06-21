from utils.bot_server import LINEWebhook
from apps.generate_reply import GenerateReply
from http.server import ThreadingHTTPServer

import os

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    dire = os.path.dirname(os.path.abspath(__file__))
    reply = GenerateReply(replyFile = f"{dire}/data/replyword.json", emotionFile = f"{dire}/data/emotion.csv")
    handler = LINEWebhook(tokenFile = f"{dire}/line.token", callback = reply.generate_message)
    server = ThreadingHTTPServer((host, port), handler.handler())
    print(f"Listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.shutdown()