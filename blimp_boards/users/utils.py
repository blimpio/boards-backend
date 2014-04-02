import hashlib


def get_gravatar_url(email):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://secure.gravatar.com/avatar/{}'.format(email_hash)


def get_profile_fields(model_class, admin_class, exclude_fields=[]):
    """
    Returns a set of additional model fields that are not already in an
    admin site's fieldsets.
    """
    fields = []
    additional_fields = []

    exclude_fields.append('id')

    for name, field_options in admin_class.fieldsets:
        fields.extend(list(field_options['fields']))

    for field in model_class._meta.fields:
        if field.name not in fields and field.name not in exclude_fields:
            additional_fields.append(field.name)

    return set(additional_fields)
