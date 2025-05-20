from django import forms
from .models import DeepfakeAnalysis

class ImageUploadForm(forms.ModelForm):
    """Form for image upload and deepfake detection."""
    class Meta:
        model = DeepfakeAnalysis
        fields = ['image']
        
    def clean_image(self):
        """Validate the uploaded image."""
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file extension
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError(
                    "Unsupported file format. Please upload a JPG or PNG image."
                )
            
            # Check file size (limit to 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError(
                    "Image file is too large. Maximum size is 10MB."
                )
                
        return image
