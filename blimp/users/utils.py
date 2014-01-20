import hashlib


def get_gravatar_url(user_email):
    GRAVATAR_URL_PREFIX = 'https://secure.gravatar.com/'

    user_hash = hashlib.md5(user_email.lower()).hexdigest()
    gravatar_url = "%savatar/%s?d=retro" % (GRAVATAR_URL_PREFIX, user_hash)

    return gravatar_url
