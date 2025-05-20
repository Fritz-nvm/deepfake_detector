import os
import logging
from transformers import ViTForImageClassification, ViTImageProcessor
import torch
from PIL import Image

logger = logging.getLogger(__name__)

class DeepfakeDetectionService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DeepfakeDetectionService, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        """Initialize the deepfake detection model and processor."""
        try:
            model_name = "prithivMLmods/Deep-Fake-Detector-Model"
            self.processor = ViTImageProcessor.from_pretrained(model_name)
            self.model = ViTForImageClassification.from_pretrained(model_name)
            self.model.eval()  # Set model to evaluation mode
            
            # Move model to GPU if available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            
            logger.info(f"Successfully loaded deepfake detection model: {model_name} on {self.device}")
        except Exception as e:
            logger.error(f"Error loading deepfake detection model: {str(e)}")
            raise
    
    def detect_deepfake(self, image_path):
        """
        Detect if an image is a deepfake.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary containing detection results
        """
        try:
            # Load and preprocess the image
            image = Image.open(image_path).convert("RGB")
            
            # Process image through the model
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Perform inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.nn.functional.softmax(logits, dim=1)
            
            # Get prediction
            predicted_class_idx = torch.argmax(logits, dim=1).item()
            predicted_label = self.model.config.id2label[predicted_class_idx]
            
            # Get confidence scores
            confidence_scores = {
                self.model.config.id2label[i]: probabilities[0][i].item() 
                for i in range(len(self.model.config.id2label))
            }
            
            # Prepare result
            result = {
                "prediction": predicted_label,
                "is_fake": predicted_label == "Fake",
                "confidence": confidence_scores[predicted_label],
                "confidence_scores": confidence_scores,
                "image_path": image_path,
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error during deepfake detection: {str(e)}")
            raise
