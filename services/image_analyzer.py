from serpapi import GoogleSearch
from duckduckgo_search import DDGS
from cachetools import TTLCache, cached
import os
import json

class ImageAnalyzer:
    def __init__(self):
        self.serpapi_key = os.getenv('SERPAPI_API_KEY')
        if not self.serpapi_key:
            raise ValueError("SERPAPI_API_KEY n'est pas définie dans les variables d'environnement")
        
        self.lens_cache = TTLCache(maxsize=100, ttl=3600)
    
    @cached(cache=lambda self: self.lens_cache)
    async def analyze_with_lens(self, image_url):
        try:
            params = {
                "api_key": self.serpapi_key,
                "engine": "google_lens",
                "url": image_url
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extraire les informations pertinentes
            visual_matches = results.get('visual_matches', [])
            knowledge_graph = results.get('knowledge_graph', {})
            
            return {
                'visual_matches': visual_matches[:5] if visual_matches else [],  # Top 5 matches
                'knowledge_graph': knowledge_graph
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de l'analyse avec Google Lens: {str(e)}")
