from django.core.exceptions import ValidationError

def validate_name(value):

    if not value.isalpha() and value:
        raise ValidationError("The Username must consist of letters only!")