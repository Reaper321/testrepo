import pytest
from src.utils import validator

def test_is_valid_email():
    assert validator.is_valid_email('example@test.com')
    assert validator.is_valid_email('foo.bar+baz@co-domain.com')
    assert not validator.is_valid_email('not-an-email')
    assert not validator.is_valid_email('')
    assert not validator.is_valid_email(None)
    assert not validator.is_valid_email('bad@.com')
    assert not validator.is_valid_email('@test.com')

def test_is_valid_url():
    assert validator.is_valid_url('http://example.com')
    assert validator.is_valid_url('https://test-domain.io/path?query=1')
    assert validator.is_valid_url('ftp://ftp.example.com/file')
    assert not validator.is_valid_url('www.example.com')
    assert not validator.is_valid_url('')
    assert not validator.is_valid_url(None)
    assert not validator.is_valid_url('http:/bad.com')

def test_format_and_validate_phone():
    assert validator.format_and_validate_phone('+1 (555) 123-4567') == '15551234567'
    assert validator.format_and_validate_phone('0044 7700 900123') == '00447700900123'
    assert validator.format_and_validate_phone('5551234') == '5551234'
    assert validator.format_and_validate_phone('(555)') is None
    assert validator.format_and_validate_phone('') is None
    assert validator.format_and_validate_phone(None) is None
    assert validator.format_and_validate_phone('1234567890123456') is None

def test_luhn_check():
    assert validator.luhn_check('4539578763621486')  # Valid Visa
    assert not validator.luhn_check('4539578763621487')  # Invalid
    assert validator.luhn_check('6011111111111117')  # Valid Discover
    assert not validator.luhn_check('')
    assert not validator.luhn_check(None)
    assert not validator.luhn_check('abcdefg')
