from flask_restx import ValidationError

def slot_range(slot_id: int):
    if slot_id<3:
        raise ValidationError


def slot_range_validator(slot_id: int):
    """
    Custom validator for slot id value range
    """
    if slot_id > 17 or slot_id < 0:
        raise ValidationError('Slot id must be between 0 and 3')


def ip_length_validator(ip: str):
    """
    Custom validator for range of number of character of an ip address
    """
    n_chars = len(ip)
    if n_chars > 15 or n_chars < 7:
        raise ValidationError('Ip address number of characters must be between 7 and 15')
