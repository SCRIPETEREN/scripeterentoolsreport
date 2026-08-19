import smtplib
import ssl
import requests
from email.mime.text import MIMEText
from rich.console import Console

console = Console()

class Sender:
    def __init__(self, config):
        self.config = config

    def send_email(self, provider_name, target, subject, body):
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.config['email_sender']
            msg['To'] = target

            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls(context=context)
                server.login(self.config['email_sender'], self.config['app_password'])
                server.sendmail(self.config['email_sender'], target, msg.as_string())
            return {"status": "sent", "provider": provider_name, "target": target}
        except Exception as e:
            return {"status": "failed", "provider": provider_name, "error": str(e)}

    def send_http(self, provider_name, url, payload):
        try:
            # Hanya simulasi untuk edukasi – tidak benar-benar mengirim
            # response = requests.post(url, json=payload, timeout=10)
            # return {"status": response.status_code, "provider": provider_name}
            return {"status": "simulated", "provider": provider_name, "url": url, "payload": payload}
        except Exception as e:
            return {"status": "failed", "provider": provider_name, "error": str(e)}

    def send_form(self, provider_name, url):
        # Simulasi form – hanya menampilkan instruksi
        return {"status": "simulated", "provider": provider_name, "note": f"Buka {url} dan isi manual"}