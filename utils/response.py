from datetime import datetime, timezone
from typing import Any, Optional


def build_response(
    status_code: int,
    data: Any = None,
    message: str = "",
    path: Optional[str] = None,
    error: Optional[str] = None,
):
    return {
        "statusCode": status_code,
        "data": data,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": path,
        "error": error,
    }
