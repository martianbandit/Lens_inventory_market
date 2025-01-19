from crewai import Agent
from langchain.tools import Tool
from services.image_analyzer import ImageAnalyzer

class LensResearchAgent(Agent):
    def __init__(self):
        self.image_analyzer = ImageAnalyzer()
        
        super().__init__(
            tools=[
                Tool(
                    name="analyze_with_lens",
                    func=self.image_analyzer.analyze_with_lens,
                    description="Analyser une image avec Google Lens"
                ),
                Tool(
                    name="search_additional_info",
                    func=self.image_analyzer.search_additional_info,
                    description="Rechercher des informations supplémentaires"
                )
            ]
        )
    
    async def research_image(self, image_url, context):
        # Analyser avec Google Lens
        lens_results = await self.image_analyzer.analyze_with_lens(image_url)
        
        # Rechercher des informations supplémentaires
        search_query = self._build_search_query(context, lens_results)
        additional_info = await self.image_analyzer.search_additional_info(search_query)
        
        return {
            'lens_analysis': lens_results,
            'additional_info': additional_info,
            'market_insights': self._extract_market_insights(lens_results)
        }
    
    def _build_search_query(self, context, lens_results):
        # Construire une requête de recherche pertinente
        main_subject = context.get('main_subject', '')
        visual_matches = lens_results.get('visual_matches', [])
        
        if visual_matches:
            relevant_terms = [match.get('title', '') for match in visual_matches[:2]]
            return f"{main_subject} {' '.join(relevant_terms)} market price features"
        
        return main_subject
    
    def _extract_market_insights(self, lens_results):
        # Extraire des informations pertinentes pour le marché
        insights = {
            'estimated_price_range': self._analyze_price_range(lens_results),
            'similar_products': self._extract_similar_products(lens_results),
            'market_categories': self._identify_categories(lens_results)
        }
        return insights
    
    def _analyze_price_range(self, results):
        # Analyser la fourchette de prix à partir des résultats
        prices = []
        for match in results.get('visual_matches', []):
            if 'price' in match:
                try:
                    prices.append(float(match['price'].replace('$', '')))
                except:
                    continue
        
        if prices:
            return {
                'min': min(prices),
                'max': max(prices),
                'average': sum(prices) / len(prices)
            }
        return None
    
    def _extract_similar_products(self, results):
        return [match.get('title') for match in results.get('visual_matches', [])[:5]]
    
    def _identify_categories(self, results):
        categories = set()
        for match in results.get('visual_matches', []):
            if 'category' in match:
                categories.add(match['category'])
        return list(categories)
