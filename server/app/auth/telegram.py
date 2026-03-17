import hashlib
import hmac
import json
from datetime import datetime, UTC
from urllib.parse import unquote, parse_qsl # будем парсить данные о пользователе для initData

from fastapi import HTTPException, status
from server.app.config import settings

def verify_telegram_init_data(init_data: str) -> dict:
    parsed = dict(parse_qsl(unquote(init_data), keep_blank_values=True))
    received_hash = parsed.pop("hash", None)

    if not received_hash:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing hash")

    auth_date = parsed.get("auth_date")
    if not auth_date:
        raise HTTPException(status_code=401, detail="Missing auth_date")
    auth_date = int(auth_date)

    now = int(datetime.now(UTC).timestamp())

    if now - auth_date > settings.TELEGRAM_TOKEN_EXPIRATION:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
        )

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed.items())
    )

    secret_key = hmac.new(
        key=b"WebAppData",
        msg=settings.BOT_TOKEN.encode(),
        digestmod=hashlib.sha256
    ).digest()

    expected_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_hash, received_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")

    user_data = json.loads(parsed.get("user", "{}"))
    return user_data
