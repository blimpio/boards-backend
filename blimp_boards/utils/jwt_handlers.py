import datetime

from rest_framework_jwt.settings import api_settings


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def jwt_payload_handler(user):
    return {
        'user_id': user.id,
        'token_version': user.token_version,
        'exp': datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
