from django.conf import settings
from django.utils.encoding import smart_text
from django.utils.six.moves.urllib.parse import unquote
from django.utils.log import getLogger

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..cards.models import Card
from ..utils.parsers import PlainTextParser
from .utils import generate_policy, generate_signature, generate_file_key
from .previews import decode_previews_payload


logger = getLogger(__name__)


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

        logger.info('Received previews payload')

        if not payload:
            logger.info('Error decoding previews payload data')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        metadata = payload.get('metadata')
        error = payload.get('error')

        if error:
            logger.info('Error found in payload data: {}'.format(error))
            return Response(status=status.HTTP_400_BAD_REQUEST)

        card_id = metadata['cardId']

        try:
            card = Card.objects.get(pk=card_id)
        except Card.DoesNotExist:
            logger.info('Card {} from payload data not found'.format(card_id))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        results = payload.get('results', [])

        for result in results['thumbnails']:
            size = result['size']
            page = str(result['page'])
            url = unquote(result['url'])

            if page == '1':
                if size['width'] == '42':
                    card.thumbnail_xs_path = url
                elif size['width'] == '200':
                    card.thumbnail_sm_path = url
                elif size['width'] == '500':
                    card.thumbnail_md_path = url
                elif size['width'] == '800':
                    card.thumbnail_lg_path = url

        if results:
            card.data = results
            card.save()

            card.update_notification_data()

        return Response(status=status.HTTP_200_OK)
