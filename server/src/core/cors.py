from typing import (
    Dict, 
    List
)

cosr_config: Dict[str, str | bool | List[str]] = {
    "origins": [
        "http://localhost:8000",    # for react dev
        "http://127.0.0.1:5500",    # for liveserver
        "https://www.google.com"    # for google
    ],
    "is_credentials_allowed": True,
    "methods": ["GET", "POST", "DELETE", "PATCH", "PUT"],
    "headers": ["*"]
}