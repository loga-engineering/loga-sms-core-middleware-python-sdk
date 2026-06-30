import os
import requests
import time
import uuid
from typing import Optional

from .models import SmsPriority, SMSSendResponse, SmsStatusResponse


class LogaSmsClient:
    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 api_key: Optional[str] = None,
                 base_url: Optional[str] = None,
                 default_sender_name: Optional[str] = None,
                 default_callback_url: Optional[str] = None,
                 timeout: Optional[int] = None):
        self.client_id = client_id or os.getenv("LOGA_SMS_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("LOGA_SMS_CLIENT_SECRET")
        self.api_key = api_key or os.getenv("LOGA_SMS_API_KEY")
        self.base_url = (base_url or os.getenv("LOGA_SMS_BASE_URL") or "https://api.sms.loga-apps.com").rstrip('/')
        self.default_sender_name = default_sender_name or os.getenv("LOGA_SMS_DEFAULT_SENDER_NAME")
        self.default_callback_url = default_callback_url or os.getenv("LOGA_SMS_DEFAULT_CALLBACK_URL")
        self.timeout = timeout or 30

        if not self.api_key:
            raise ValueError("LOGA SMS API Key is required")

        self.access_token: Optional[str] = None
        self.token_expires_at: float = 0
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def _ensure_authenticated(self):
        now = time.time()
        if self.access_token and now < self.token_expires_at - 60:
            return

        if not self.client_id or not self.client_secret:
            return

        data = {
            "grant_type": "client_credentials",
            "clientId": self.client_id,
            "clientSecret": self.client_secret
        }

        response = requests.post(
            f"{self.base_url}/oauth/v1/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=self.timeout
        )
        response.raise_for_status()

        token_data = response.json()
        self.access_token = token_data["access_token"]
        self.token_expires_at = now + token_data["expires_in"]
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    def _invalidate_token(self):
        self.access_token = None
        self.token_expires_at = 0
        self.session.headers.pop("Authorization", None)

    def send(self,
             to: str,
             message: str,
             priority: SmsPriority = SmsPriority.QUEUED,
             sender_name: Optional[str] = None,
             callback_url: Optional[str] = None,
             idempotency_key: Optional[str] = None) -> SMSSendResponse:
        def _attempt():
            self._ensure_authenticated()

            payload = {
                "receiverAddress": to,
                "message": message,
                "priority": priority.value,
                "senderName": sender_name or self.default_sender_name,
                "callbackUrl": callback_url or self.default_callback_url
            }

            headers = {
                "Idempotency-Key": idempotency_key or str(uuid.uuid4()),
                "X-API-KEY": self.api_key
            }

            response = self.session.post(
                f"{self.base_url}/api/smsmessaging/v1/outbound/send",
                json={k: v for k, v in payload.items() if v is not None},
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            return SMSSendResponse(**data)

        try:
            return _attempt()
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 401:
                self._invalidate_token()
                return _attempt()
            raise

    def check_status(self, external_ref_no: Optional[str] = None, idempotency_key: Optional[str] = None) -> SmsStatusResponse:
        if not external_ref_no and not idempotency_key:
            raise ValueError("Either externalRefNo or idempotencyKey is required")

        def _attempt():
            self._ensure_authenticated()

            headers = {
                "X-API-KEY": self.api_key
            }

            params = {"externalRefNo": external_ref_no} if external_ref_no else {"idempotencyKey": idempotency_key}

            response = self.session.get(
                f"{self.base_url}/api/smsmessaging/v1/status",
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            return SmsStatusResponse(**data)

        try:
            return _attempt()
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 401:
                self._invalidate_token()
                return _attempt()
            raise
