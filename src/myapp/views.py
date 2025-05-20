from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.conf import settings
import os
import logging

from .forms import ImageUploadForm
from .models import DeepfakeAnalysis
from .services import DeepfakeDetectionService

logger = logging.getLogger(__name__)

# Initialize the detection service
detection_service = DeepfakeDetectionService()

def index(request):
    """Render the main page with upload form."""
    return render(request, 'deepfake_detector/index.html')

class DeepfakeDetectionView(View):
    """Class-based view for deepfake detection with web interface."""
    
    def get(self, request):
        """Render the detection form."""
        form = ImageUploadForm()
        return render(request, 'deepfake_detector/detect.html', {'form': form})
    
    def post(self, request):
        """Process image upload and perform detection."""
        form = ImageUploadForm(request.POST, request.FILES)
        
        if not form.is_valid():
            return render(request, 'deepfake_detector/detect.html', {
                'form': form,
                'error': 'Invalid form submission'
            })
        
        try:
            # Save form to get the image path
            analysis = form.save(commit=False)
            
            # Get the full path to the saved image
            image_path = os.path.join(settings.MEDIA_ROOT, str(analysis.image))
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            
            # Save the model instance to save the file
            analysis.save()
            
            # Perform deepfake detection
            result = detection_service.detect_deepfake(image_path)
            
            # Update the analysis object with results
            analysis.is_fake = result['is_fake']
            analysis.confidence = result['confidence']
            analysis.prediction = result['prediction']
            analysis.confidence_real = result['confidence_scores'].get('Real', 0.0)
            analysis.confidence_fake = result['confidence_scores'].get('Fake', 0.0)
            analysis.save()
            
            return render(request, 'deepfake_detector/result.html', {
                'result': result,
                'analysis': analysis,
                'image_url': analysis.image.url
            })
            
        except Exception as e:
            logger.error(f"Error during deepfake detection: {str(e)}")
            return render(request, 'deepfake_detector/detect.html', {
                'form': form,
                'error': f"Error processing image: {str(e)}"
            })

def recent_analyses(request):
    """Display recent analyses."""
    analyses = DeepfakeAnalysis.objects.order_by('-created_at')[:10]
    return render(request, 'deepfake_detector/recent.html', {'analyses': analyses})

# API endpoint for programmatic access
def detect_api(request):
    """API endpoint for deepfake detection."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)
    
    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image file provided'}, status=400)
    
    try:
        form = ImageUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({'error': form.errors['image'][0]}, status=400)
        
        # Save form to get the image path
        analysis = form.save(commit=False)
        
        # Get the full path to the saved image
        image_path = os.path.join(settings.MEDIA_ROOT, str(analysis.image))
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        
        # Save the model instance to save the file
        analysis.save()
        
        # Perform deepfake detection
        result = detection_service.detect_deepfake(image_path)
        
        # Update the analysis object with results
        analysis.is_fake = result['is_fake']
        analysis.confidence = result['confidence']
        analysis.prediction = result['prediction']
        analysis.confidence_real = result['confidence_scores'].get('Real', 0.0)
        analysis.confidence_fake = result['confidence_scores'].get('Fake', 0.0)
        analysis.save()
        
        # Add image URL to result
        result['image_url'] = request.build_absolute_uri(analysis.image.url)
        
        return JsonResponse(result)
    
    except Exception as e:
        logger.error(f"Error during API deepfake detection: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
