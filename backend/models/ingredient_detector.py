import torch
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer, DetrImageProcessor, DetrForObjectDetection
from PIL import Image
import re
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IngredientDetector:
    def __init__(self):
        self.model_name = "nlpconnect/vit-gpt2-image-captioning"
        self.detr_model_name = "facebook/detr-resnet-50"
        
        # Initialize image captioning model
        try:
            logger.info("Loading image captioning model...")
            self.caption_model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
            self.caption_processor = ViTImageProcessor.from_pretrained(self.model_name)
            self.caption_tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            logger.info("Image captioning model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load captioning model: {e}")
            self.caption_model = None
        
        # Initialize object detection model
        try:
            logger.info("Loading object detection model...")
            self.detr_processor = DetrImageProcessor.from_pretrained(self.detr_model_name)
            self.detr_model = DetrForObjectDetection.from_pretrained(self.detr_model_name)
            logger.info("Object detection model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load object detection model: {e}")
            self.detr_model = None
        
        # Common food ingredients that might be detected
        self.food_keywords = {
            'apple', 'banana', 'orange', 'lemon', 'lime', 'tomato', 'potato', 'onion',
            'garlic', 'carrot', 'broccoli', 'spinach', 'lettuce', 'cucumber', 'pepper',
            'cheese', 'milk', 'butter', 'egg', 'bread', 'chicken', 'beef', 'pork',
            'fish', 'salmon', 'tuna', 'shrimp', 'pasta', 'rice', 'beans', 'corn',
            'mushroom', 'avocado', 'strawberry', 'blueberry', 'grape', 'pineapple',
            'yogurt', 'cream', 'flour', 'sugar', 'salt', 'oil', 'vinegar', 'herbs',
            'basil', 'parsley', 'cilantro', 'rosemary', 'thyme', 'oregano'
        }
        
        # COCO class names that are food-related
        self.coco_food_classes = {
            'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
            'pizza', 'donut', 'cake', 'chair', 'bottle', 'wine glass', 'cup', 'fork',
            'knife', 'spoon', 'bowl'
        }

    def detect(self, image: Image.Image) -> List[Dict[str, any]]:
        """Detect ingredients from image using both captioning and object detection."""
        ingredients = []
        
        # Method 1: Image captioning
        if self.caption_model:
            caption_ingredients = self._detect_from_caption(image)
            ingredients.extend(caption_ingredients)
        
        # Method 2: Object detection
        if self.detr_model:
            detection_ingredients = self._detect_from_objects(image)
            ingredients.extend(detection_ingredients)
        
        # Remove duplicates and sort by confidence
        unique_ingredients = self._deduplicate_ingredients(ingredients)
        
        # If no ingredients detected, provide fallback
        if not unique_ingredients:
            unique_ingredients = [
                {"name": "mixed vegetables", "confidence": 0.5},
                {"name": "pantry items", "confidence": 0.3}
            ]
        
        return unique_ingredients[:10]  # Return top 10

    def _detect_from_caption(self, image: Image.Image) -> List[Dict[str, any]]:
        """Extract ingredients from image caption."""
        try:
            # Generate caption
            pixel_values = self.caption_processor(image, return_tensors="pt").pixel_values
            
            with torch.no_grad():
                output_ids = self.caption_model.generate(
                    pixel_values,
                    max_length=50,
                    num_beams=4,
                    early_stopping=True
                )
            
            caption = self.caption_tokenizer.decode(output_ids[0], skip_special_tokens=True)
            logger.info(f"Generated caption: {caption}")
            
            # Extract food items from caption
            ingredients = []
            words = re.findall(r'\b\w+\b', caption.lower())
            
            for word in words:
                if word in self.food_keywords:
                    ingredients.append({
                        "name": word,
                        "confidence": 0.8
                    })
            
            return ingredients
            
        except Exception as e:
            logger.error(f"Error in caption-based detection: {e}")
            return []

    def _detect_from_objects(self, image: Image.Image) -> List[Dict[str, any]]:
        """Detect food objects using DETR model."""
        try:
            # Process image
            inputs = self.detr_processor(images=image, return_tensors="pt")
            
            with torch.no_grad():
                outputs = self.detr_model(**inputs)
            
            # Post-process detections
            target_sizes = torch.tensor([image.size[::-1]])
            results = self.detr_processor.post_process_object_detection(
                outputs, target_sizes=target_sizes, threshold=0.5
            )[0]
            
            ingredients = []
            for score, label in zip(results["scores"], results["labels"]):
                class_name = self.detr_model.config.id2label[label.item()]
                if class_name in self.coco_food_classes:
                    ingredients.append({
                        "name": class_name,
                        "confidence": score.item()
                    })
            
            return ingredients
            
        except Exception as e:
            logger.error(f"Error in object detection: {e}")
            return []

    def _deduplicate_ingredients(self, ingredients: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """Remove duplicate ingredients and combine confidences."""
        ingredient_dict = {}
        
        for ingredient in ingredients:
            name = ingredient["name"]
            confidence = ingredient["confidence"]
            
            if name in ingredient_dict:
                # Take the higher confidence
                ingredient_dict[name] = max(ingredient_dict[name], confidence)
            else:
                ingredient_dict[name] = confidence
        
        # Convert back to list and sort by confidence
        result = [
            {"name": name, "confidence": confidence}
            for name, confidence in ingredient_dict.items()
        ]
        
        return sorted(result, key=lambda x: x["confidence"], reverse=True) 