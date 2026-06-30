from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SmsPriority(str, Enum):
    INSTANT = "INSTANT"
    TRANSACTION = "TRANSACTION"
    CAMPAIGN = "CAMPAIGN"
    QUEUED = "QUEUED"


class SMSRequestStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    SENT = "SENT"
    FAILED = "FAILED"
    ERROR = "ERROR"
    CAMPAIGN = "CAMPAIGN"


@dataclass
class SMSSendRequest:
    receiverAddress: str
    message: str
    priority: SmsPriority
    senderName: Optional[str] = None
    callbackUrl: Optional[str] = None


@dataclass
class SMSSendResponse:
    externalRefNo: str
    status: SMSRequestStatus
    message: str


@dataclass
class SmsStatusResponse:
    externalRefNo: str
    status: SMSRequestStatus
    receiverAddress: str
    createdAt: str
    updatedAt: str
    message: str


@dataclass
class OAuth2TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
