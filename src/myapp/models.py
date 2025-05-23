from django.db import models
import uuid
import os

# def get_upload_path(instance, filename):
#     """Generate a unique path for uploaded images."""
#     ext = filename.split('.')[-1]
#     filename = f"{uuid.uuid4()}.{ext}"
#     return os.path.join('uploads', filename)

class DeepfakeAnalysis(models.Model):
    """Model to store deepfake detection results."""
    image = models.ImageField(upload_to='media/')
    is_fake = models.BooleanField(default=False)
    confidence = models.FloatField(default=0.0)
    prediction = models.CharField(max_length=50, default='Unknown')
    confidence_real = models.FloatField(default=0.0)
    confidence_fake = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis {self.id}: {'Fake' if self.is_fake else 'Real'} ({self.confidence:.2f})"
