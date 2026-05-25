import re
from typing import Optional

def is_valid_email(email: Optional[str]) -> bool:
    if not isinstance(email, str):
        return False
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(email_regex, email) is not None

def is_valid_url(url: Optional[str]) -> bool:
    if not isinstance(url, str):
        return False
    url_regex = r"^(https?|ftp):\/\/[\w.-]+(\.[\w.-]+)+([\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])?$"
    return re.match(url_regex, url) is not None

def format_and_validate_phone(phone: Optional[str]) -> Optional[str]:
    if not isinstance(phone, str):
        return None
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 7 or len(digits) > 15:
        return None
    return digits

def luhn_check(card_number: Optional[str]) -> bool:
    if not isinstance(card_number, str):
        return False
    digits = re.sub(r"\D", "", card_number)
    sum_ = 0
    alt = False
    for d in reversed(digits):
        n = int(d)
        if alt:
            n *= 2
            if n > 9:
                n -= 9
        sum_ += n
        alt = not alt
    return sum_ % 10 == 0 if digits else False
