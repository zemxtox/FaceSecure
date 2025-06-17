from rest_framework import serializers
from .models import Face

class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ('id', 'name', 'image', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 