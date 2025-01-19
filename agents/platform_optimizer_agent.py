from crewai import Agent
from langchain.tools import Tool
from typing import Dict, List

class PlatformOptimizerAgent(Agent):
    def __init__(self):
        super().__init__(
            tools=[
                Tool(
                    name="optimize_for_platform",
                    func=self.optimize_for_platform,
                    description="Optimise une annonce pour une plateforme spécifique"
                )
            ]
        )
        
        self.platform_constraints = {
            'facebook': {
                'title_length': 100,
                'description_length': 5000,
                'tags_count': 30
            },
            'instagram': {
                'title_length': 80,
                'description_length': 2200,
                'tags_count': 30
            },
            'leboncoin': {
                'title_length': 70,
                'description_length': 4000,
                'tags_count': 15
            }
        }
    
    async def optimize_for_platform(self, listing: Dict, platform: str) -> Dict:
        """Optimise une annonce pour une plateforme spécifique"""
        
        constraints = self.platform_constraints.get(platform.lower(), {})
        if not constraints:
            return listing  # Retourner l'annonce non modifiée si la plateforme n'est pas reconnue
        
        optimized_listing = {
            'title': self._optimize_title(listing['title'], constraints['title_length']),
            'description': self._optimize_description(listing['description'], 
                                                   constraints['description_length'],
                                                   platform),
            'highlights': self._optimize_highlights(listing['highlights'], platform),
            'tags': self._optimize_tags(listing['tags'], 
                                      constraints['tags_count'],
                                      platform),
            'call_to_action': self._optimize_cta(listing['call_to_action'], platform),
            'platform_specific': self._add_platform_specific(listing, platform)
        }
        
        return optimized_listing
    
    def _optimize_title(self, title: str, max_length: int) -> str:
        """Optimise le titre pour la plateforme"""
        if len(title) <= max_length:
            return title
            
        # Tronquer intelligemment
        words = title.split()
        optimized = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                optimized.append(word)
                current_length += len(word) + 1
            else:
                break
        
        return " ".join(optimized)
    
    def _optimize_description(self, description: str, max_length: int, platform: str) -> str:
        """Optimise la description pour la plateforme"""
        if platform.lower() == 'instagram':
            # Ajouter des emojis stratégiques pour Instagram
            description = self._add_emojis(description)
        
        if len(description) <= max_length:
            return description
        
        # Tronquer intelligemment en préservant les paragraphes importants
        paragraphs = description.split('\n\n')
        optimized = []
        current_length = 0
        
        for para in paragraphs:
            if current_length + len(para) + 2 <= max_length:
                optimized.append(para)
                current_length += len(para) + 2
            else:
                break
        
        return "\n\n".join(optimized)
    
    def _optimize_highlights(self, highlights: List[str], platform: str) -> List[str]:
        """Optimise les points forts pour la plateforme"""
        if platform.lower() == 'instagram':
            # Ajouter des emojis aux points forts
            return [f"✨ {highlight}" for highlight in highlights]
        return highlights
    
    def _optimize_tags(self, tags: List[str], max_count: int, platform: str) -> List[str]:
        """Optimise les tags pour la plateforme"""
        if platform.lower() == 'instagram':
            # Formatter pour Instagram
            tags = [f"#{tag.replace(' ', '')}" for tag in tags]
        
        # Trier par pertinence et limiter le nombre
        return sorted(tags, key=len)[:max_count]
    
    def _optimize_cta(self, cta: str, platform: str) -> str:
        """Optimise l'appel à l'action pour la plateforme"""
        platform_ctas = {
            'facebook': "👉 Cliquez pour plus d'infos !",
            'instagram': "DM pour plus d'infos 📩",
            'leboncoin': "Contactez-moi pour plus d'informations"
        }
        
        return platform_ctas.get(platform.lower(), cta)
    
    def _add_platform_specific(self, listing: Dict, platform: str) -> Dict:
        """Ajoute des éléments spécifiques à la plateforme"""
        if platform.lower() == 'instagram':
            return {
                'hashtag_groups': self._create_hashtag_groups(listing['tags']),
                'story_format': self._create_story_format(listing)
            }
        elif platform.lower() == 'facebook':
            return {
                'marketplace_category': self._determine_marketplace_category(listing),
                'condition_category': self._determine_condition_category(listing)
            }
        return {}
    
    def _add_emojis(self, text: str) -> str:
        """Ajoute des emojis stratégiques au texte"""
        emoji_mapping = {
            'prix': '💰',
            'qualité': '✨',
            'nouveau': '🆕',
            'contact': '📱',
            'livraison': '🚚'
        }
        
        for keyword, emoji in emoji_mapping.items():
            if keyword in text.lower():
                text = text.replace(keyword, f"{emoji} {keyword}")
        
        return text
    
    def _create_hashtag_groups(self, tags: List[str]) -> List[str]:
        """Crée des groupes de hashtags optimisés pour Instagram"""
        hashtags = [tag.replace(' ', '') for tag in tags]
        groups = []
        current_group = []
        current_length = 0
        
        for tag in hashtags:
            if current_length + len(tag) + 2 <= 500:  # Limite Instagram par commentaire
                current_group.append(f"#{tag}")
                current_length += len(tag) + 2
            else:
                groups.append(" ".join(current_group))
                current_group = [f"#{tag}"]
                current_length = len(tag) + 2
        
        if current_group:
            groups.append(" ".join(current_group))
        
        return groups
    
    def _create_story_format(self, listing: Dict) -> Dict:
        """Crée un format optimisé pour les stories Instagram"""
        return {
            'headline': self._optimize_title(listing['title'], 40),
            'price_display': self._format_price_for_story(listing),
            'key_features': listing['highlights'][:3],
            'story_cta': "Swipe Up ⬆️"
        }
    
    def _determine_marketplace_category(self, listing: Dict) -> str:
        """Détermine la catégorie Marketplace appropriée"""
        # Logique de détermination de catégorie à implémenter
        return "Autre"
    
    def _determine_condition_category(self, listing: Dict) -> str:
        """Détermine la catégorie d'état pour Marketplace"""
        condition_mapping = {
            'Neuf': 'NEW',
            'Très bon état': 'LIKE_NEW',
            'Bon état': 'GOOD',
            'État satisfaisant': 'FAIR',
            'Pour pièces': 'POOR'
        }
        
        return condition_mapping.get(listing.get('condition', ''), 'GOOD')
    
    def _format_price_for_story(self, listing: Dict) -> str:
        """Formate le prix pour l'affichage en story"""
        # Logique de formatage de prix à implémenter
        return "Prix sur demande"
