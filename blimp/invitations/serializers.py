from rest_framework import serializers

from .models import SignupRequest


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignupRequest
        fields = ('email',)
