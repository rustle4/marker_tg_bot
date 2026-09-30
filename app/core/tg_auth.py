import hashlib
import hmac
import json
import time
from dataclasses import dataclass
from urllib.parse import parse_qsl

from fastapi import Header, HTTPException, status

from app.core.config import settings


@dataclass(slots=True, frozen=True)
class TelegramInitData:
    telegram_id: int
    username: str | None
    first_name: str | None
    last_name: str | None


def validate_init_data(init_data: str) -> TelegramInitData:
    if not settings.TELEGRAM_TOKEN:
        raise HTTPException(status_code=500, detail="TELEGRAM_TOKEN is not configured")

    parsed = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = parsed.pop("hash", None)
    parsed.pop("signature", None)
    if not received_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Telegram hash"
        )

    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(parsed.items())
    )
    secret_key = hmac.new(
        b"WebAppData",
        settings.TELEGRAM_TOKEN.encode(),
        hashlib.sha256,
    ).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(calculated_hash, received_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Telegram data"
        )

    try:
        auth_date = int(parsed["auth_date"])
        telegram_user = json.loads(parsed["user"])
        telegram_id = int(telegram_user["id"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Telegram data"
        ) from exc

    if time.time() - auth_date > settings.TELEGRAM_INIT_DATA_MAX_AGE_SECONDS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Telegram data expired"
        )

    return TelegramInitData(
        telegram_id=telegram_id,
        username=telegram_user.get("username"),
        first_name=telegram_user.get("first_name"),
        last_name=telegram_user.get("last_name"),
    )


def get_init_data(
    telegram_init_data: str | None = Header(default=None),
    dev_telegram_id: int | None = Header(default=None),
) -> TelegramInitData:
    if settings.ALLOW_DEV_AUTH and dev_telegram_id is not None:
        return TelegramInitData(
            telegram_id=dev_telegram_id,
            username="dev_user",
            first_name="Dev",
            last_name=None,
        )

    if not telegram_init_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Telegram Init Data header",
        )

    return validate_init_data(telegram_init_data)
