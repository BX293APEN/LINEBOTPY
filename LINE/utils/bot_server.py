import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

class LINEWebhook:
    LINE_API_URL = "https://api.line.me/v2/bot/message/reply"
    def __init__(self, token, callback):
        self.generate_message = callback
        self.LINE_CHANNEL_TOKEN = token
    
    def reply_to_line(self, reply_token, text):
        payload = json.dumps(
            {
                "replyToken": reply_token,
                "messages": [
                    {
                        "type": "text",
                        "text": text,
                    }
                ],
            }
        ).encode("UTF-8")

        req = urllib.request.Request(
            self.LINE_API_URL,
            data=payload,
            method="POST",
            headers={
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": f"Bearer {self.LINE_CHANNEL_TOKEN}",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as res:
                res.read()
        except urllib.error.HTTPError as e:
            print(f"[LINE API ERROR] status={e.code} body={e.read().decode('UTF-8', 'replace')}")

    def handler(self):
        generate_message    = self.generate_message
        reply_to_line       = self.reply_to_line

        class WebhookHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                # 動作確認用（LINE Webhookは使わないが、ヘルスチェック等のために用意）
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=UTF-8")
                self.end_headers()
                self.wfile.write("LINE BOT webhook server is running.".encode("UTF-8"))

            def log_message(self, format, *args):
                # 標準のアクセスログ出力（必要に応じてここで抑制・カスタマイズできる）
                print(f"[{self.address_string()}] {format % args}")

            def do_POST(self):
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)

                try:
                    data = json.loads(body.decode("UTF-8"))
                    event_data = data["events"][0]
                    if "replyToken" in event_data:
                        reply_text = generate_message(event_data["message"]["text"])
                        reply_to_line(event_data["replyToken"], reply_text)

                except Exception as e:
                    # Webhook処理中の例外でサーバーを落とさない（GAS版の例外時の挙動に合わせ、
                    # こちらでも200を返してLINE側からのリトライ連打を避ける）
                    print(f"[doPost ERROR] {e!r}")

                # LINE Webhookは200が返らないと再送・エラー扱いになるため必ず200を返す
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()
        
        return WebhookHandler
