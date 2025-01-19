from crewai import Agent
from langchain.tools import Tool
from typing import Dict, List

class CopywriterAgent(Agent):
    def __init__(self):
        super().__init__(
            tools=[
                Tool(
                    name="generate_listing",
                    func=self.generate_listing,
                    description="Génère une annonce attractive"
                )
            ]
        )
    
    async def generate_listing(self, product_data: Dict) -> Dict:
        """Génère une annonce complète basée sur les données du produit"""
        
        listing = {
            'title': self._generate_title(product_data),
            'description': self._generate_description(product_data),
            'highlights': self._generate_highlights(product_data),
            'tags': self._generate_tags(product_data),
            'call_to_action': self._generate_cta(product_data)
        }
        
        return listing
    
    def _generate_title(self, data: Dict) -> str:
        """Génère un titre accrocheur"""
        product_info = data['product_information']
        market_analysis = data['market_analysis']
        
        product_name = product_info['product_name']
        condition = product_info['condition']
        
        # Construire un titre attractif
        title_elements = [
            product_name,
            condition if condition != "Bon état" else "",
            self._get_unique_selling_point(market_analysis)
        ]
        
        return " | ".join(filter(None, title_elements))
    
    def _generate_description(self, data: Dict) -> str:
        """Génère une description détaillée et engageante"""
        product_info = data['product_information']
        tech_details = data['technical_details']
        
        description_parts = [
            self._create_opening_hook(product_info),
            self._create_main_description(product_info, tech_details),
            self._create_technical_section(tech_details),
            self._create_market_context(data['market_analysis'])
        ]
        
        return "\n\n".join(filter(None, description_parts))
    
    def _generate_highlights(self, data: Dict) -> List[str]:
        """Génère une liste de points forts"""
        highlights = []
        tech_details = data['technical_details']
        
        # Ajouter les caractéristiques principales
        if 'features' in tech_details:
            highlights.extend(tech_details['features'][:5])
        
        # Ajouter des points sur l'état et la qualité
        condition = data['product_information']['condition']
        if condition:
            highlights.append(f"État: {condition}")
        
        return highlights
    
    def _generate_tags(self, data: Dict) -> List[str]:
        """Génère des tags pertinents pour l'annonce"""
        tags = set()
        
        # Ajouter les catégories de marché
        market_categories = data['market_analysis'].get('market_categories', [])
        tags.update(market_categories)
        
        # Ajouter le type de produit
        product_name = data['product_information']['product_name']
        tags.add(product_name.lower())
        
        # Ajouter l'état
        condition = data['product_information']['condition']
        if condition:
            tags.add(condition.lower())
        
        return list(tags)
    
    def _generate_cta(self, data: Dict) -> str:
        """Génère un appel à l'action personnalisé"""
        price_range = data['market_analysis'].get('price_range', {})
        if price_range and 'average' in price_range:
            return f"À vous pour seulement {price_range['average']}€ ! Contactez-nous maintenant !"
        return "Contactez-nous pour plus d'informations !"
    
    def _get_unique_selling_point(self, market_analysis: Dict) -> str:
        """Identifie et retourne un point de vente unique"""
        if 'price_competitiveness' in market_analysis:
            if market_analysis['price_competitiveness'] == 'competitive':
                return "Prix Compétitif"
        return ""
    
    def _create_opening_hook(self, product_info: Dict) -> str:
        """Crée une accroche initiale"""
        return f"Découvrez ce magnifique {product_info['product_name']} en {product_info['condition']} !"
    
    def _create_main_description(self, product_info: Dict, tech_details: Dict) -> str:
        """Crée la description principale"""
        description = []
        
        if 'specifications' in tech_details:
            specs = tech_details['specifications']
            description.append("Caractéristiques principales:")
            description.extend([f"- {spec}" for spec in specs[:5]])
        
        return "\n".join(description)
    
    def _create_technical_section(self, tech_details: Dict) -> str:
        """Crée la section technique"""
        if 'features' in tech_details:
            features = tech_details['features']
            return "Détails techniques:\n" + "\n".join([f"• {feature}" for feature in features])
        return ""
    
    def _create_market_context(self, market_analysis: Dict) -> str:
        """Crée le contexte de marché"""
        price_range = market_analysis.get('price_range', {})
        if price_range:
            return f"Prix du marché entre {price_range.get('min', 0)}€ et {price_range.get('max', 0)}€"
        return ""
