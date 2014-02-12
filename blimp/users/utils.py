import hashlib


def get_gravatar_url(user_email):
    GRAVATAR_URL_PREFIX = 'https://secure.gravatar.com/'
    email = user_email.lower().encode('utf-8')
    user_hash = hashlib.md5(email).hexdigest()
    gravatar_url = "%savatar/%s?d=retro" % (GRAVATAR_URL_PREFIX, user_hash)

    return gravatar_url


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
