from django.db import models
from django.core.validators import FileExtensionValidator

class UploadedFile(models.Model):
    file = models.FileField(
        upload_to='uploads/',  # Store files in the 'uploads/' directory
        validators=[
            FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'mp4', 'avi', 'jpg', 'jpeg', 'png'])
        ]  # Restrict file types
    )
    upload_date = models.DateTimeField(auto_now_add=True)
    is_deepfake = models.BooleanField(null=True, blank=True)  # Result of analysis (null until analyzed)
    analysis_details = models.TextField(blank=True)  # Store details from the analysis
    filename = models.CharField(max_length=255) #stores the name of the file

    def __str__(self):
        return self.filename #display the filename

    class Meta:
        ordering = ['-upload_date']  # Show latest uploads first