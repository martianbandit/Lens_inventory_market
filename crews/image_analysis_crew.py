from crewai import Crew, Task, Agent
from services.object_detection import ObjectDetectionService
from services.image_analyzer import ImageAnalyzer
from agents.vision_agent import VisionAgent
from agents.lens_research_agent import LensResearchAgent
from agents.data_aggregation_agent import DataAggregationAgent

class ImageAnalysisCrew:
    def __init__(self):
        self.object_detection = ObjectDetectionService()
        self.image_analyzer = ImageAnalyzer()
        
        # Initialisation des agents
        self.vision_agent = Agent(
            role='Vision Analyst',
            goal='Analyser précisément les objets dans les images',
            backstory='Expert en vision par ordinateur et analyse d\'images',
            agent_type=VisionAgent
        )
        
        self.lens_agent = Agent(
            role='Lens Researcher',
            goal='Rechercher des informations détaillées via Google Lens',
            backstory='Spécialiste en recherche visuelle et analyse de produits',
            agent_type=LensResearchAgent
        )
        
        self.data_agent = Agent(
            role='Data Aggregator',
            goal='Agréger et structurer les informations collectées',
            backstory='Expert en synthèse et organisation de données',
            agent_type=DataAggregationAgent
        )

    async def analyze_image(self, image_file):
        crew = Crew(
            agents=[self.vision_agent, self.lens_agent, self.data_agent],
            tasks=[
                Task(
                    description='Détecter et analyser les objets dans l\'image',
                    agent=self.vision_agent,
                    expected_output="Liste des objets détectés avec leurs caractéristiques"
                ),
                Task(
                    description='Rechercher des informations via Google Lens',
                    agent=self.lens_agent,
                    expected_output="Informations détaillées sur les objets identifiés"
                ),
                Task(
                    description='Compiler et structurer toutes les informations',
                    agent=self.data_agent,
                    expected_output="Données structurées pour la génération d'annonces"
                )
            ]
        )
        
        result = await crew.kickoff()
        return result
