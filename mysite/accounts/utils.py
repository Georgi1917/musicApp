
def append_validators(form, field_names, validator):

    for name in field_names:

        if name in form.fields:
            form.fields[name].validators.append(validator)


def remove_help_text(form):

    for name, value in form.fields.items():
        value.help_text = ""