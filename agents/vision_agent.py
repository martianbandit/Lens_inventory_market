from crewai import Agent
from langchain.tools import Tool
from services.object_detection import ObjectDetectionService

class VisionAgent(Agent):
    def __init__(self):
        self.object_detection = ObjectDetectionService()
        
        super().__init__(
            tools=[
                Tool(
                    name="detect_objects",
                    func=self.object_detection.detect_objects,
                    description="Détecte les objets dans une image"
                ),
                Tool(
                    name="process_realtime",
                    func=self.object_detection.process_realtime,
                    description="Traite un flux vidéo en temps réel"
                )
            ]
        )
    
    async def analyze_image(self, image_data):
        # Utiliser les outils pour analyser l'image
        detections = await self.object_detection.detect_objects(image_data)
        
        # Analyser et structurer les résultats
        analysis = {
            'objects': detections,
            'main_subject': self._identify_main_subject(detections),
            'scene_context': self._analyze_scene(detections)
        }
        
        return analysis
    
    def _identify_main_subject(self, detections):
        # Identifier l'objet principal basé sur la taille et la confiance
        if not detections:
            return None
            
        return max(detections, key=lambda x: x['confidence'])['class']
    
    def _analyze_scene(self, detections):
        # Analyser le contexte de la scène
        object_classes = [d['class'] for d in detections]
        return {
            'object_count': len(detections),
            'unique_objects': list(set(object_classes))
        }
