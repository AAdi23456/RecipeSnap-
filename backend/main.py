from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import tempfile
import uuid
from PIL import Image
import io

from models.ingredient_detector import IngredientDetector
from models.recipe_generator import RecipeGenerator
from models.text_to_speech import TextToSpeech

app = FastAPI(title="RecipeSnap Backend", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs("temp_files", exist_ok=True)
os.makedirs("audio_files", exist_ok=True)

# Mount static files for audio
app.mount("/audio", StaticFiles(directory="audio_files"), name="audio")

# Initialize AI models
ingredient_detector = IngredientDetector()
recipe_generator = RecipeGenerator()
text_to_speech = TextToSpeech()

class RecipeRequest(BaseModel):
    ingredients: List[str]
    regenerate: Optional[bool] = False

class TTSRequest(BaseModel):
    text: str

class IngredientResponse(BaseModel):
    name: str
    confidence: float

class Recipe(BaseModel):
    title: str
    ingredients: List[str]
    instructions: List[str]
    cookingTime: str

@app.get("/")
async def root():
    return {"message": "RecipeSnap Backend API", "status": "running"}

@app.post("/detect-ingredients")
async def detect_ingredients(image: UploadFile = File(...)):
    """Detect ingredients from uploaded image using AI vision models."""
    try:
        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        
        # Detect ingredients
        ingredients = ingredient_detector.detect(pil_image)
        
        return {"ingredients": ingredients, "count": len(ingredients)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/generate-recipe")
async def generate_recipe(request: RecipeRequest):
    """Generate recipe based on available ingredients using local LLM."""
    try:
        if not request.ingredients:
            raise HTTPException(status_code=400, detail="No ingredients provided")
        
        # Generate recipe using local LLM
        recipe = recipe_generator.generate(
            ingredients=request.ingredients,
            regenerate=request.regenerate
        )
        
        return {"recipe": recipe}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")

@app.post("/text-to-speech")
async def convert_text_to_speech(request: TTSRequest):
    """Convert recipe text to speech audio file."""
    try:
        if not request.text:
            raise HTTPException(status_code=400, detail="No text provided")
        
        # Generate unique filename
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join("audio_files", audio_filename)
        
        # Convert text to speech
        text_to_speech.convert(request.text, audio_path)
        
        # Return URL to audio file
        audio_url = f"/audio/{audio_filename}"
        return {"audio_url": audio_url, "filename": audio_filename}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting text to speech: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models": {
            "ingredient_detector": ingredient_detector.model_name,
            "recipe_generator": recipe_generator.model_name,
            "text_to_speech": "gtts"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 