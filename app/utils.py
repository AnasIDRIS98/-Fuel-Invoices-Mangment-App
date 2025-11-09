# utils.py - helpers for decimals and pdf export
from decimal import Decimal, getcontext
getcontext().prec = 28
def to_decimal(x):
    try:
        return Decimal(str(x))
    except Exception:
        return Decimal('0')
def format_decimal(d: Decimal):
    return format(d, 'f')
def generate_invoice_pdf_bytes(row: dict):
    return None
