#!/usr/bin/env python3
"""
RecipeSnap Backend Startup Script
This script downloads and caches AI models on first run.
"""

import os
import sys
import logging
from transformers import (
    VisionEncoderDecoderModel, 
    ViTImageProcessor, 
    AutoTokenizer,
    DetrImageProcessor,
    DetrForObjectDetection,
    AutoModelForCausalLM
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_models():
    """Download and cache all required AI models."""
    models_to_download = [
        {
            "name": "Image Captioning Model",
            "model_name": "nlpconnect/vit-gpt2-image-captioning",
            "components": [
                ("VisionEncoderDecoderModel", VisionEncoderDecoderModel),
                ("ViTImageProcessor", ViTImageProcessor),
                ("AutoTokenizer", AutoTokenizer)
            ]
        },
        {
            "name": "Object Detection Model", 
            "model_name": "facebook/detr-resnet-50",
            "components": [
                ("DetrImageProcessor", DetrImageProcessor),
                ("DetrForObjectDetection", DetrForObjectDetection)
            ]
        },
        {
            "name": "Recipe Generation Model",
            "model_name": "microsoft/DialoGPT-medium",
            "components": [
                ("AutoTokenizer", AutoTokenizer),
                ("AutoModelForCausalLM", AutoModelForCausalLM)
            ]
        }
    ]
    
    logger.info("Starting model download process...")
    
    for model_info in models_to_download:
        logger.info(f"Downloading {model_info['name']}...")
        
        try:
            for component_name, component_class in model_info["components"]:
                logger.info(f"  Loading {component_name}...")
                component_class.from_pretrained(model_info["model_name"])
                logger.info(f"  ✓ {component_name} loaded successfully")
            
            logger.info(f"✓ {model_info['name']} downloaded successfully")
            
        except Exception as e:
            logger.error(f"✗ Failed to download {model_info['name']}: {e}")
            logger.warning(f"The application will use fallback methods for {model_info['name']}")
    
    logger.info("Model download process completed!")

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'torch', 'transformers', 'PIL', 'fastapi', 'uvicorn', 
        'gtts', 'numpy', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {', '.join(missing_packages)}")
        logger.error("Please install missing packages using: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main startup function."""
    logger.info("RecipeSnap Backend Startup")
    logger.info("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Download models
    download_models()
    
    logger.info("=" * 40)
    logger.info("Setup complete! You can now start the backend server.")
    logger.info("Run: python main.py")

if __name__ == "__main__":
    main() 