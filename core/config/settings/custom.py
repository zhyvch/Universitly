from typing import Dict, List

PHONE_NUMBER_ACCESS_CONTROL: Dict[str, List[str]] = {
    'allowlist': [r'\d*'],
    'denylist': [r'\+7\d*'], # blacklist has priority over whitelist
}

USE_E164: bool = True

TRUNCATE_TOO_LONG_PHONE_NUMBERS: bool = True
