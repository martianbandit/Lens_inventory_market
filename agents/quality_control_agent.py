from crewai import Agent
from langchain.tools import Tool
from typing import Dict, List
import re

class QualityControlAgent(Agent):
    def __init__(self):
        super().__init__(
            tools=[
                Tool(
                    name="verify_listing",
                    func=self.verify_listing,
                    description="Vérifie et améliore la qualité d'une annonce"
                )
            ]
        )
        
        self.quality_checks = {
            'spelling': self._check_spelling,
            'grammar': self._check_grammar,
            'completeness': self._check_completeness,
            'consistency': self._check_consistency,
            'seo': self._check_seo,
            'compliance': self._check_compliance
        }
    
    async def verify_listing(self, listing: Dict, platform: str) -> Dict:
        """Vérifie et améliore la qualité d'une annonce"""
        
        # Effectuer tous les contrôles de qualité
        quality_report = self._run_quality_checks(listing, platform)
        
        # Améliorer l'annonce si nécessaire
        if not all(check['passed'] for check in quality_report['checks']):
            listing = self._improve_listing(listing, quality_report)
        
        return {
            'improved_listing': listing,
            'quality_report': quality_report
        }
    
    def _run_quality_checks(self, listing: Dict, platform: str) -> Dict:
        """Exécute tous les contrôles de qualité"""
        checks = []
        overall_score = 0
        
        for check_name, check_func in self.quality_checks.items():
            result = check_func(listing, platform)
            checks.append({
                'name': check_name,
                'passed': result['passed'],
                'score': result['score'],
                'issues': result['issues']
            })
            overall_score += result['score']
        
        return {
            'overall_score': overall_score / len(self.quality_checks),
            'checks': checks,
            'platform': platform
        }
    
    def _check_spelling(self, listing: Dict, platform: str) -> Dict:
        """Vérifie l'orthographe"""
        issues = []
        
        # Vérification simple des mots courants mal orthographiés
        common_mistakes = {
            'acceuil': 'accueil',
            'language': 'langage',
            'developp': 'développ'
        }
        
        for text in [listing['title'], listing['description']]:
            for mistake, correction in common_mistakes.items():
                if mistake in text.lower():
                    issues.append(f"Correction suggérée: {mistake} -> {correction}")
        
        score = 1.0 if not issues else 0.8
        return {
            'passed': len(issues) == 0,
            'score': score,
            'issues': issues
        }
    
    def _check_grammar(self, listing: Dict, platform: str) -> Dict:
        """Vérifie la grammaire"""
        issues = []
        
        # Vérification simple des erreurs grammaticales courantes
        grammar_patterns = [
            (r'je peut', 'je peux'),
            (r'sa va', 'ça va'),
            (r'ces bon', "c'est bon")
        ]
        
        for text in [listing['title'], listing['description']]:
            for pattern, correction in grammar_patterns:
                if re.search(pattern, text.lower()):
                    issues.append(f"Correction suggérée: {pattern} -> {correction}")
        
        score = 1.0 if not issues else 0.8
        return {
            'passed': len(issues) == 0,
            'score': score,
            'issues': issues
        }
    
    def _check_completeness(self, listing: Dict, platform: str) -> Dict:
        """Vérifie que l'annonce est complète"""
        issues = []
        required_fields = ['title', 'description', 'highlights', 'tags']
        
        for field in required_fields:
            if field not in listing or not listing[field]:
                issues.append(f"Champ manquant ou vide: {field}")
        
        # Vérifier la longueur minimale de la description
        if len(listing['description']) < 100:
            issues.append("Description trop courte (min. 100 caractères)")
        
        score = 1.0 if not issues else 0.7
        return {
            'passed': len(issues) == 0,
            'score': score,
            'issues': issues
        }
    
    def _check_consistency(self, listing: Dict, platform: str) -> Dict:
        """Vérifie la cohérence des informations"""
        issues = []
        
        # Vérifier la cohérence entre le titre et la description
        title_keywords = set(listing['title'].lower().split())
        desc_keywords = set(listing['description'].lower().split())
        
        if not title_keywords.intersection(desc_keywords):
            issues.append("Le titre et la description semblent déconnectés")
        
        # Vérifier la cohérence des tags
        for tag in listing['tags']:
            if not (tag.lower() in listing['title'].lower() or 
                   tag.lower() in listing['description'].lower()):
                issues.append(f"Tag non pertinent: {tag}")
        
        score = 1.0 if not issues else 0.9
        return {
            'passed': len(issues) == 0,
            'score': score,
            'issues': issues
        }
    
    def _check_seo(self, listing: Dict, platform: str) -> Dict:
        """Vérifie l'optimisation SEO"""
        issues = []
        
        # Vérifier la présence de mots-clés importants
        if 'tags' in listing:
            main_keywords = set(listing['tags'])
            title_words = set(listing['title'].lower().split())
            desc_words = set(listing['description'].lower().split())
            
            missing_keywords = main_keywords - (title_words | desc_words)
            if missing_keywords:
                issues.append(f"Mots-clés manquants dans le contenu: {missing_keywords}")
        
        # Vérifier la densité des mots-clés
        if 'description' in listing:
            word_count = len(listing['description'].split())
            if word_count < 50:
                issues.append("Contenu trop court pour une bonne optimisation SEO")
        
        score = 1.0 if not issues else 0.8
        return {
            'passed': len(issues) == 0,
            'score': score,
            'issues': issues
        }
    
    def _check_compliance(self, listing: Dict, platform: str) -> Dict:
        """Vérifie la conformité aux règles de la plateforme"""
        issues = []
        
        # Vérifier les restrictions spécifiques à la plateforme
        platform_restrictions = {
            'facebook': {
                'title_length': 100,
                'forbidden_words': ['gratuit', 'urgent']
            },
            'instagram': {
                'title_length': 80,
                'max_tags': 30
            },
            'leboncoin': {
                'title_length': 70,
                'max_description': 4000
            }
        }
        
        if platform.lower() in platform_restrictions:
            restrictions = platform_restrictions[platform.lower()]
            
            # Vérifier la longueur du titre
            if len(listing['title']) > restrictions['title_length']:
                issues.append(f"Titre trop long pour {platform}")
            
            # Vérifier les mots interdits
            if 'forbidden_words' in restrictions:
                for word in restrictions['forbidden_words']:
                    if word in listing['title'].lower() or word in listing['description'].lower():
                        issues.append(f"Mot interdit détecté: {word}")
        
        score = 1.0 if not issues else 0.7
        return {
            'passed': len(issues) == 0,
            'score': score,
            'issues': issues
        }
    
    def _improve_listing(self, listing: Dict, quality_report: Dict) -> Dict:
        """Améliore l'annonce en fonction du rapport de qualité"""
        improved_listing = listing.copy()
        
        for check in quality_report['checks']:
            if not check['passed']:
                if check['name'] == 'spelling':
                    improved_listing = self._fix_spelling(improved_listing, check['issues'])
                elif check['name'] == 'grammar':
                    improved_listing = self._fix_grammar(improved_listing, check['issues'])
                elif check['name'] == 'completeness':
                    improved_listing = self._complete_listing(improved_listing, check['issues'])
                elif check['name'] == 'seo':
                    improved_listing = self._optimize_seo(improved_listing, check['issues'])
        
        return improved_listing
    
    def _fix_spelling(self, listing: Dict, issues: List[str]) -> Dict:
        """Corrige les erreurs d'orthographe"""
        improved = listing.copy()
        
        for issue in issues:
            if '->' in issue:
                mistake, correction = issue.split('->')
                mistake = mistake.strip().split(':')[-1].strip()
                correction = correction.strip()
                
                improved['title'] = improved['title'].replace(mistake, correction)
                improved['description'] = improved['description'].replace(mistake, correction)
        
        return improved
    
    def _fix_grammar(self, listing: Dict, issues: List[str]) -> Dict:
        """Corrige les erreurs grammaticales"""
        improved = listing.copy()
        
        for issue in issues:
            if '->' in issue:
                mistake, correction = issue.split('->')
                mistake = mistake.strip().split(':')[-1].strip()
                correction = correction.strip()
                
                improved['title'] = improved['title'].replace(mistake, correction)
                improved['description'] = improved['description'].replace(mistake, correction)
        
        return improved
    
    def _complete_listing(self, listing: Dict, issues: List[str]) -> Dict:
        """Complète les informations manquantes"""
        improved = listing.copy()
        
        for issue in issues:
            if "Champ manquant" in issue:
                field = issue.split(':')[-1].strip()
                if field == 'highlights' and not improved.get('highlights'):
                    improved['highlights'] = self._generate_highlights(improved)
                elif field == 'tags' and not improved.get('tags'):
                    improved['tags'] = self._generate_tags(improved)
        
        return improved
    
    def _optimize_seo(self, listing: Dict, issues: List[str]) -> Dict:
        """Optimise le contenu pour le SEO"""
        improved = listing.copy()
        
        for issue in issues:
            if "Mots-clés manquants" in issue:
                keywords = issue.split(':')[-1].strip()
                improved['description'] = self._integrate_keywords(
                    improved['description'],
                    eval(keywords)  # Convertir la string en set
                )
        
        return improved
    
    def _generate_highlights(self, listing: Dict) -> List[str]:
        """Génère des points forts à partir de la description"""
        # Exemple simple - à améliorer selon les besoins
        return ["Point fort 1", "Point fort 2", "Point fort 3"]
    
    def _generate_tags(self, listing: Dict) -> List[str]:
        """Génère des tags à partir du contenu"""
        # Exemple simple - à améliorer selon les besoins
        words = listing['title'].lower().split()
        return list(set(words))[:5]
    
    def _integrate_keywords(self, description: str, keywords: set) -> str:
        """Intègre naturellement les mots-clés manquants dans la description"""
        # Exemple simple - à améliorer selon les besoins
        for keyword in keywords:
            if keyword not in description.lower():
                description += f" {keyword}"
        return description
