from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
from services.object_detection import ObjectDetectionService
from services.image_analyzer import ImageAnalyzer
from dotenv import load_dotenv
import os
import io
import aiohttp

load_dotenv()

app = FastAPI(title="Lens Inventory Market")
object_detection = ObjectDetectionService()
image_analyzer = ImageAnalyzer()

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        # Lire le contenu de l'image
        contents = await file.read()
        
        # Détecter les objets dans l'image
        detections = await object_detection.detect_objects(contents)
        
        # Créer une URL temporaire pour l'image (simulé pour l'exemple)
        image_url = "https://example.com/temp.jpg"  # À remplacer par un vrai service de stockage
        
        # Analyser avec Google Lens
        lens_results = await image_analyzer.analyze_with_lens(image_url)
        
        # Combiner les résultats
        results = {
            "object_detection": detections,
            "lens_analysis": lens_results
        }
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Lens Inventory Market"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
