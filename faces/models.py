from django.db import models
from django.conf import settings

class Face(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='faces/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='faces')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    class Meta:
        verbose_name = 'Face'
        verbose_name_plural = 'Faces'
        ordering = ['-created_at']