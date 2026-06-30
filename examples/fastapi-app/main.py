import os
from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv

from loga_sms_sdk import LogaSmsClient
from loga_sms_sdk.models import SmsPriority, SMSSendResponse, SmsStatusResponse

load_dotenv()

app = FastAPI(title="Loga SMS - Python Sample", version="1.0.0")

client = LogaSmsClient(
    client_id=os.getenv("LOGA_SMS_CLIENT_ID"),
    client_secret=os.getenv("LOGA_SMS_CLIENT_SECRET"),
    api_key=os.getenv("LOGA_SMS_API_KEY"),
    base_url=os.getenv("LOGA_SMS_BASE_URL"),
    default_sender_name=os.getenv("LOGA_SMS_DEFAULT_SENDER_NAME"),
    default_callback_url=os.getenv("LOGA_SMS_DEFAULT_CALLBACK_URL"),
)


@app.post("/sms/send/default")
def send_default(to: str = Query(...), message: str = Query(...)):
    try:
        response: SMSSendResponse = client.send(to, message)
        return {
            "externalRefNo": response.externalRefNo,
            "status": response.status,
            "message": response.message,
            "mode": "default sender + default callback",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sms/send/custom-sender")
def send_custom_sender(
    to: str = Query(...),
    message: str = Query(...),
    sender_name: str = Query(...),
):
    try:
        response: SMSSendResponse = client.send(
            to, message, sender_name=sender_name
        )
        return {
            "externalRefNo": response.externalRefNo,
            "status": response.status,
            "message": response.message,
            "mode": f"custom sender: {sender_name}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sms/send/custom-callback")
def send_custom_callback(
    to: str = Query(...),
    message: str = Query(...),
    callback_url: str = Query(...),
):
    try:
        response: SMSSendResponse = client.send(
            to, message, callback_url=callback_url
        )
        return {
            "externalRefNo": response.externalRefNo,
            "status": response.status,
            "message": response.message,
            "mode": f"custom callback: {callback_url}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sms/send/full")
def send_full(
    to: str = Query(...),
    message: str = Query(...),
    sender_name: str | None = Query(None),
    callback_url: str | None = Query(None),
    priority: str = Query(default="QUEUED"),
):
    try:
        sms_priority = SmsPriority(priority.upper())
        response: SMSSendResponse = client.send(
            to,
            message,
            priority=sms_priority,
            sender_name=sender_name,
            callback_url=callback_url,
        )
        return {
            "externalRefNo": response.externalRefNo,
            "status": response.status,
            "message": response.message,
            "mode": "full control",
            "priority": priority,
        }
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid priority. Use: INSTANT, TRANSACTION, CAMPAIGN, QUEUED",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sms/status")
def check_status(
    external_ref_no: str = Query(None),
    idempotency_key: str = Query(None),
):
    try:
        status: SmsStatusResponse = client.check_status(external_ref_no, idempotency_key)
        return {
            "externalRefNo": status.externalRefNo,
            "status": status.status,
            "receiverAddress": status.receiverAddress,
            "createdAt": status.createdAt,
            "updatedAt": status.updatedAt,
            "message": status.message,
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
