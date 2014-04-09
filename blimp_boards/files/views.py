from django.conf import settings
from django.utils.encoding import smart_text
from django.utils.six.moves.urllib.parse import unquote

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..cards.models import Card
from ..utils.parsers import PlainTextParser
from .utils import generate_policy, generate_signature, generate_file_key
from .previews import decode_previews_payload


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


class FilePreviewsWebhook(APIView):
    authentication_classes = ()
    permission_classes = ()
    parser_classes = (PlainTextParser, )

    def post(self, request):
        payload = decode_previews_payload(request.DATA)

        if not payload:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            metadata = payload['metadata']
            card = Card.objects.get(pk=metadata['cardId'])
        except Card.DoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        error = payload.get('error')

        if not error:
            results = payload.get('results', [])

            for result in results:
                size = result['size']
                url = unquote(result['url'])

                if size == '200':
                    card.thumbnail_sm_path = url

                if size == '500':
                    card.thumbnail_md_path = url

                if size == '800':
                    card.thumbnail_lg_path = url

            if results:
                card.save()

        return Response(status=status.HTTP_200_OK)
