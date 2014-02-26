from django.conf import settings
from django.utils.encoding import smart_text
from rest_framework.views import APIView
from rest_framework.response import Response

from .utils import generate_policy, generate_signature, generate_file_key


class SignS3FileUploadAPIView(APIView):
    """
    Generates data needed to upload a file directly to AWS S3,
    including key, policy, signature, and access key.
    """
    def get(self, request):
        access_key = settings.AWS_ACCESS_KEY_ID
        secret_key = settings.AWS_SECRET_ACCESS_KEY
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        file_name = request.QUERY_PARAMS.get('name', '$filename')
        mime_type = request.QUERY_PARAMS.get('type')
        file_size = request.QUERY_PARAMS.get('size')

        policy = generate_policy(bucket, mime_type, file_size)
        signature = generate_signature(policy, secret_key)

        key = generate_file_key(name=file_name, user=request.user)

        params = {
            'access_key': access_key,
            'bucket_url': 'https://s3.amazonaws.com/{}'.format(bucket),
            "policy": smart_text(policy),
            "signature": smart_text(signature),
            "key": key,
            "success_action_redirect": "/"
        }

        return Response(params)
