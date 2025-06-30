from flask_restx import ValidationError

def slot_range(slot_id: int):
    if slot_id<3:
        raise ValidationError


def slot_range_validator(age: int):
    """
    Custom validator for age range
    """
    if age > 17 or age < 0:
        raise ValidationError('Slot id must be between 0 and 3')
