import re
from typing import Optional

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-]+)\.([a-zA-Z]{2,})$')
URL_REGEX = re.compile(
    r'^(https?|ftp)://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[^\s]*)?$'
)


def is_valid_email(email: Optional[str]) -> bool:
    if not email:
        return False
    return EMAIL_REGEX.match(email) is not None


def is_valid_url(url: Optional[str]) -> bool:
    if not url:
        return False
    return URL_REGEX.match(url) is not None


def format_and_validate_phone(phone: Optional[str], min_length: int = 10, max_length: int = 15) -> Optional[str]:
    if not phone:
        return None
    digits = ''.join(filter(str.isdigit, phone))
    if min_length <= len(digits) <= max_length:
        return digits
    return None


def luhn_check(card_number: Optional[str]) -> bool:
    if not card_number:
        return False
    digits = [int(d) for d in str(card_number) if d.isdigit()]
    if not digits:
        return False
    checksum = 0
    odd = False
    for d in reversed(digits):
        if odd:
            d = d * 2
            if d > 9:
                d -= 9
        checksum += d
        odd = not odd
    return checksum % 10 == 0
