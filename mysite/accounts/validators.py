from django.core.exceptions import ValidationError

def validate_name(value):

    if not value.isalpha() and value:
        raise ValidationError("The Name must consist of letters only!")
    

def validate_email(value):

    if value.split("@")[1] != "gmail.com":
        raise ValidationError("Please use a Gmail.com email!")