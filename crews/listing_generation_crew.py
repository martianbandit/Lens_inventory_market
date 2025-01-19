from crewai import Crew, Task, Agent
from agents.copywriter_agent import CopywriterAgent
from agents.platform_optimizer_agent import PlatformOptimizerAgent
from agents.quality_control_agent import QualityControlAgent

class ListingGenerationCrew:
    def __init__(self):
        self.copywriter = Agent(
            role='Copywriter',
            goal='Créer des descriptions attractives et précises',
            backstory='Expert en rédaction publicitaire et marketing',
            agent_type=CopywriterAgent
        )
        
        self.optimizer = Agent(
            role='Platform Optimizer',
            goal='Optimiser le contenu pour chaque plateforme sociale',
            backstory='Spécialiste en marketing digital multi-plateformes',
            agent_type=PlatformOptimizerAgent
        )
        
        self.quality_control = Agent(
            role='Quality Controller',
            goal='Vérifier et améliorer la qualité des annonces',
            backstory='Expert en contrôle qualité et optimisation de contenu',
            agent_type=QualityControlAgent
        )

    async def generate_listing(self, analysis_data):
        crew = Crew(
            agents=[self.copywriter, self.optimizer, self.quality_control],
            tasks=[
                Task(
                    description='Créer une description attractive basée sur l\'analyse',
                    agent=self.copywriter,
                    expected_output="Description engageante et détaillée du produit"
                ),
                Task(
                    description='Optimiser le contenu pour différentes plateformes',
                    agent=self.optimizer,
                    expected_output="Versions optimisées pour chaque plateforme sociale"
                ),
                Task(
                    description='Vérifier et améliorer la qualité finale',
                    agent=self.quality_control,
                    expected_output="Annonce finale vérifiée et améliorée"
                )
            ]
        )
        
        result = await crew.kickoff()
        return result
