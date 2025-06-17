from django.db import models
from django.conf import settings
from cameras.models import Camera
from faces.models import Face

class Detection(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='detections')
    detected_face = models.ForeignKey(Face, on_delete=models.SET_NULL, null=True, related_name='detections')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    confidence_score = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='detections/', null=True, blank=True)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Detection on {self.camera.name} at {self.timestamp}"

    class Meta:
        verbose_name = 'Detection'
        verbose_name_plural = 'Detections'
        ordering = ['-timestamp']
