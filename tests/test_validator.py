import pytest
from src.utils import validator

def test_is_valid_email():
    assert validator.is_valid_email('test@example.com')
    assert not validator.is_valid_email('invalid-email')
    assert not validator.is_valid_email('')
    assert not validator.is_valid_email(None)
    assert validator.is_valid_email('a_b.c-d@sub.dom.co')

def test_is_valid_url():
    assert validator.is_valid_url('http://example.com')
    assert validator.is_valid_url('https://example.com/path/file')
    assert validator.is_valid_url('ftp://foo.bar.site')
    assert not validator.is_valid_url('just-text')
    assert not validator.is_valid_url('')
    assert not validator.is_valid_url(None)

def test_format_and_validate_phone():
    # US style number
    assert validator.format_and_validate_phone('(415) 555-6789') == '4155556789'
    # Short international
    assert validator.format_and_validate_phone('+49 151 23456789', min_length=9) == '4915123456789'
    # Russian (11 digits)
    assert validator.format_and_validate_phone('+7 (912) 345-67-89', min_length=11, max_length=12) == '79123456789'
    # Too short
    assert validator.format_and_validate_phone('12345') is None
    # Too long
    assert validator.format_and_validate_phone('1' * 20) is None
    # None or blank
    assert validator.format_and_validate_phone(None) is None
    assert validator.format_and_validate_phone('') is None

def test_luhn_check():
    # Real valid card numbers
    assert validator.luhn_check('4539578763621486')  # Visa
    assert validator.luhn_check('6011514433546201')  # Discover
    # Invalid card number
    assert not validator.luhn_check('1234567890123456')
    # Empty or None
    assert not validator.luhn_check('')
    assert not validator.luhn_check(None)
    # Spaces and dashes
    assert validator.luhn_check('6011-5144-3354-6201')

