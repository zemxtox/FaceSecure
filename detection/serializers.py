from rest_framework import serializers
from .models import Detection
from cameras.serializers import CameraSerializer
from faces.serializers import FaceSerializer

class DetectionSerializer(serializers.ModelSerializer):
    camera = CameraSerializer(read_only=True)
    detected_face = FaceSerializer(read_only=True)

    class Meta:
        model = Detection
        fields = ('id', 'camera', 'detected_face', 'timestamp', 'status', 
                 'confidence_score', 'image', 'notification_sent')
        read_only_fields = ('id', 'timestamp', 'status', 'confidence_score', 
                           'image', 'notification_sent')

class DetectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detection
        fields = ('camera',) 