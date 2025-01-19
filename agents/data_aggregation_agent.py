from crewai import Agent
from langchain.tools import Tool
from typing import Dict, List
import json

class DataAggregationAgent(Agent):
    def __init__(self):
        super().__init__(
            tools=[
                Tool(
                    name="aggregate_data",
                    func=self.aggregate_data,
                    description="Agrège et structure les données d'analyse"
                )
            ]
        )
    
    async def aggregate_data(self, vision_data: Dict, lens_data: Dict) -> Dict:
        """Agrège les données des différentes sources d'analyse"""
        
        aggregated_data = {
            'product_information': self._compile_product_info(vision_data, lens_data),
            'market_analysis': self._compile_market_analysis(lens_data),
            'technical_details': self._compile_technical_details(vision_data, lens_data),
            'metadata': self._generate_metadata()
        }
        
        return aggregated_data
    
    def _compile_product_info(self, vision_data: Dict, lens_data: Dict) -> Dict:
        """Compile les informations principales du produit"""
        return {
            'main_category': vision_data.get('main_subject'),
            'detected_objects': vision_data.get('objects', []),
            'visual_matches': lens_data.get('lens_analysis', {}).get('visual_matches', []),
            'product_name': self._determine_product_name(vision_data, lens_data),
            'condition': self._assess_condition(vision_data)
        }
    
    def _compile_market_analysis(self, lens_data: Dict) -> Dict:
        """Compile l'analyse de marché"""
        market_insights = lens_data.get('market_insights', {})
        return {
            'price_range': market_insights.get('estimated_price_range'),
            'similar_products': market_insights.get('similar_products', []),
            'market_categories': market_insights.get('market_categories', []),
            'competition_analysis': self._analyze_competition(lens_data)
        }
    
    def _compile_technical_details(self, vision_data: Dict, lens_data: Dict) -> Dict:
        """Compile les détails techniques"""
        return {
            'specifications': self._extract_specifications(lens_data),
            'dimensions': self._extract_dimensions(vision_data),
            'features': self._extract_features(lens_data)
        }
    
    def _determine_product_name(self, vision_data: Dict, lens_data: Dict) -> str:
        """Détermine le nom le plus approprié pour le produit"""
        lens_matches = lens_data.get('lens_analysis', {}).get('visual_matches', [])
        if lens_matches:
            return lens_matches[0].get('title', vision_data.get('main_subject', ''))
        return vision_data.get('main_subject', '')
    
    def _assess_condition(self, vision_data: Dict) -> str:
        """Évalue l'état du produit basé sur l'analyse visuelle"""
        # Logique d'évaluation à implémenter
        return "Bon état"  # Par défaut
    
    def _analyze_competition(self, lens_data: Dict) -> Dict:
        """Analyse la concurrence basée sur les données de marché"""
        return {
            'market_saturation': 'medium',  # À implémenter
            'price_competitiveness': 'competitive'  # À implémenter
        }
    
    def _extract_specifications(self, lens_data: Dict) -> List[str]:
        """Extrait les spécifications techniques"""
        specs = []
        for match in lens_data.get('lens_analysis', {}).get('visual_matches', []):
            if 'specifications' in match:
                specs.extend(match['specifications'])
        return list(set(specs))
    
    def _extract_dimensions(self, vision_data: Dict) -> Dict:
        """Extrait les dimensions si disponibles"""
        # À implémenter avec une logique plus sophistiquée
        return {}
    
    def _extract_features(self, lens_data: Dict) -> List[str]:
        """Extrait les caractéristiques principales"""
        features = set()
        for match in lens_data.get('lens_analysis', {}).get('visual_matches', []):
            if 'features' in match:
                features.update(match['features'])
        return list(features)
    
    def _generate_metadata(self) -> Dict:
        """Génère les métadonnées de l'analyse"""
        return {
            'analysis_version': '1.0',
            'confidence_score': self._calculate_confidence_score(),
            'timestamp': self._get_timestamp()
        }
    
    def _calculate_confidence_score(self) -> float:
        """Calcule un score de confiance pour l'analyse"""
        # À implémenter avec une logique plus sophistiquée
        return 0.85
    
    def _get_timestamp(self) -> str:
        """Retourne le timestamp actuel"""
        from datetime import datetime
        return datetime.utcnow().isoformat()
