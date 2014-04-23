from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        read_only_fields = ('created_by', 'modified_by', )
        fields = ('id', 'content', 'created_by', 'modified_by',
                  'date_created', 'date_modified')
