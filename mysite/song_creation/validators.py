from django.core.exceptions import ValidationError

def validate_file_is_mp3(value):

    print(value)

    if str(value).split(".")[-1] != "mp3":
        raise ValidationError("The file must be mp3!")