"""
Entity Extractor
Extracts key entities and indicators from case descriptions
"""

import re
from datetime import datetime

class EntityExtractor:
    def __init__(self):
        self.version = "1.0.0"
    
    def extract(self, description: str, location: str = '') -> dict:
        """Extract entities and indicators"""
        description_lower = description.lower()
        
        return {
            'location': self._extract_location(description, location),
            'timeframe': self._extract_timeframe(description_lower),
            'victim_age': self._extract_age(description_lower),
            'perpetrator_relationship': self._extract_relationship(description_lower),
            'medical_indicators': self._has_medical_indicators(description_lower),
            'legal_indicators': self._has_legal_indicators(description_lower),
            'psychological_state': self._assess_psychological_state(description_lower)
        }
    
    def _extract_location(self, description: str, provided_location: str) -> str:
        """Extract location from text"""
        if provided_location:
            return provided_location
        
        # Simple location extraction (can be enhanced with NER)
        location_patterns = [
            r'in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'at ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, description)
            if match:
                return match.group(1)
        
        return 'Unknown'
    
    def _extract_timeframe(self, description: str) -> str:
        """Extract when incident occurred"""
        time_indicators = {
            'right now': 'Immediate',
            'happening now': 'Immediate',
            'currently': 'Immediate',
            'today': 'Today',
            'tonight': 'Today',
            'this morning': 'Today',
            'yesterday': 'Recent (1-2 days)',
            'last night': 'Recent (1-2 days)',
            'last week': 'Recent (1 week)',
            'few days ago': 'Recent (few days)'
        }
        
        for indicator, timeframe in time_indicators.items():
            if indicator in description:
                return timeframe
        
        return 'Unspecified'
    
    def _extract_age(self, description: str) -> int:
        """Extract victim age if mentioned"""
        age_pattern = r'(\d+)\s*(?:years?\s*old|yr|y\.o\.)'
        match = re.search(age_pattern, description)
        
        if match:
            return int(match.group(1))
        
        # Check for age-related keywords
        if any(word in description for word in ['child', 'kid', 'minor']):
            return 12  # Estimated child age
        
        return None
    
    def _extract_relationship(self, description: str) -> str:
        """Extract perpetrator relationship"""
        relationships = {
            'husband': 'Intimate Partner',
            'wife': 'Intimate Partner',
            'boyfriend': 'Intimate Partner',
            'girlfriend': 'Intimate Partner',
            'partner': 'Intimate Partner',
            'father': 'Family Member',
            'mother': 'Family Member',
            'brother': 'Family Member',
            'sister': 'Family Member',
            'uncle': 'Family Member',
            'aunt': 'Family Member',
            'boss': 'Authority Figure',
            'teacher': 'Authority Figure',
            'stranger': 'Stranger',
            'neighbor': 'Acquaintance'
        }
        
        for keyword, relationship in relationships.items():
            if keyword in description:
                return relationship
        
        return 'Unknown'
    
    def _has_medical_indicators(self, description: str) -> bool:
        """Check for medical attention indicators"""
        medical_keywords = [
            'bleeding', 'blood', 'injured', 'hurt', 'pain', 'broken',
            'bruise', 'wound', 'hospital', 'doctor', 'medical', 'sick'
        ]
        
        return any(keyword in description for keyword in medical_keywords)
    
    def _has_legal_indicators(self, description: str) -> bool:
        """Check for legal/police involvement indicators"""
        legal_keywords = [
            'police', 'report', 'crime', 'illegal', 'law', 'arrest',
            'court', 'lawyer', 'attorney', 'justice'
        ]
        
        return any(keyword in description for keyword in legal_keywords)
    
    def _assess_psychological_state(self, description: str) -> str:
        """Assess psychological state from language"""
        states = {
            'Severe Distress': ['terrified', 'traumatized', 'can\'t cope', 'want to die', 'suicide'],
            'High Anxiety': ['scared', 'afraid', 'anxious', 'panic', 'worried', 'frightened'],
            'Depression': ['hopeless', 'helpless', 'depressed', 'sad', 'crying', 'alone'],
            'Anger': ['angry', 'furious', 'rage', 'hate', 'mad'],
            'Confusion': ['confused', 'don\'t know', 'unsure', 'lost']
        }
        
        for state, keywords in states.items():
            if any(keyword in description for keyword in keywords):
                return state
        
        return 'Stable'
    
    def is_loaded(self) -> bool:
        return True
