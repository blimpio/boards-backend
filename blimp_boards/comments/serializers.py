from rest_framework import serializers

from ..users.serializers import NestedUserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    created_by = NestedUserSerializer(read_only=True)
    modified_by = NestedUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_by', 'modified_by',
                  'date_created', 'date_modified')
