from django.core.exceptions import ValidationError

def validate_name(value):

    if not value.isalpha() and value:
        raise ValidationError("The Name must consist of letters only!")
    
