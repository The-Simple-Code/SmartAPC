class SMSClient:
    def __init__(self):
        self.provider = None
        self.api_key = None
        self.api_secret = None
    def init_app(self, app):
        self.provider = app.config.get("SMS_PROVIDER", "mock")
        self.api_key = app.config.get("SMS_API_KEY", "")
        self.api_secret = app.config.get("SMS_API_SECRET", "")
    def send(self, to: str, text: str) -> bool:
        print(f"[SMS:{self.provider}] -> {to}: {text}")
        return True

sms_client = SMSClient()
