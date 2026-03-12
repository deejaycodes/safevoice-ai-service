"""
Urgency Classifier Model
Classifies case urgency: critical, high, medium, low
"""

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from datetime import datetime

class UrgencyClassifier:
    def __init__(self):
        self.version = "1.0.0"
        self.model = None
        self.vectorizer = None
        self.last_trained = None
        self.load_model()
    
    def load_model(self):
        """Load trained model or initialize new one"""
        model_path = 'models/saved/urgency_classifier.joblib'
        vectorizer_path = 'models/saved/urgency_vectorizer.joblib'
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            self.last_trained = datetime.fromtimestamp(os.path.getmtime(model_path)).isoformat()
        else:
            # Initialize with default model
            self.vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 3))
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.last_trained = None
    
    def predict(self, description: str, incident_type: str) -> dict:
        """
        Predict urgency level
        
        Returns:
        {
            'urgency': 'critical|high|medium|low',
            'confidence': float,
            'classification': str
        }
        """
        # Rule-based classification for now (will be ML-based after training)
        urgency, confidence = self._rule_based_urgency(description, incident_type)
        
        return {
            'urgency': urgency,
            'confidence': confidence,
            'classification': self._classify_incident(description, incident_type)
        }
    
    def _rule_based_urgency(self, description: str, incident_type: str) -> tuple:
        """Rule-based urgency until model is trained"""
        description_lower = description.lower()
        
        # Critical indicators
        critical_keywords = [
            'bleeding', 'unconscious', 'weapon', 'knife', 'gun', 
            'hospital', 'emergency', 'dying', 'kill', 'suicide',
            'right now', 'happening now', 'currently', 'at this moment'
        ]
        
        # High urgency indicators
        high_keywords = [
            'threatened', 'beaten', 'injured', 'hurt', 'pain',
            'scared', 'afraid', 'hiding', 'locked', 'trapped',
            'today', 'tonight', 'this morning'
        ]
        
        # Medium urgency indicators
        medium_keywords = [
            'yesterday', 'last night', 'last week', 'recently',
            'worried', 'concerned', 'uncomfortable', 'unsafe'
        ]
        
        # Check for critical
        critical_count = sum(1 for keyword in critical_keywords if keyword in description_lower)
        if critical_count >= 2:
            return 'critical', 0.95
        elif critical_count == 1:
            return 'critical', 0.85
        
        # Check for high
        high_count = sum(1 for keyword in high_keywords if keyword in description_lower)
        if high_count >= 3:
            return 'high', 0.90
        elif high_count >= 1:
            return 'high', 0.75
        
        # Check for medium
        medium_count = sum(1 for keyword in medium_keywords if keyword in description_lower)
        if medium_count >= 1:
            return 'medium', 0.70
        
        # Default to low
        return 'low', 0.60
    
    def _classify_incident(self, description: str, incident_type: str) -> str:
        """Classify the type of incident"""
        description_lower = description.lower()
        
        classifications = {
            'Physical Violence': ['hit', 'punch', 'kick', 'beat', 'slap', 'hurt', 'injured'],
            'Sexual Violence': ['rape', 'sexual', 'assault', 'molest', 'abuse', 'touched'],
            'Emotional Abuse': ['threaten', 'insult', 'yell', 'scream', 'control', 'manipulate'],
            'Child Labor': ['work', 'labor', 'child', 'forced', 'exploitation'],
            'FGM': ['cutting', 'circumcision', 'fgm', 'mutilation'],
            'Domestic Violence': ['husband', 'wife', 'partner', 'home', 'family'],
            'Trafficking': ['traffick', 'sold', 'forced', 'transport', 'exploit']
        }
        
        for classification, keywords in classifications.items():
            if any(keyword in description_lower for keyword in keywords):
                return classification
        
        return incident_type or 'General Violence'
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.vectorizer is not None
    
    def train(self, X_train, y_train):
        """Train the model with new data"""
        # Transform text to features
        X_features = self.vectorizer.fit_transform(X_train)
        
        # Train model
        self.model.fit(X_features, y_train)
        
        # Save model
        os.makedirs('models/saved', exist_ok=True)
        joblib.dump(self.model, 'models/saved/urgency_classifier.joblib')
        joblib.dump(self.vectorizer, 'models/saved/urgency_vectorizer.joblib')
        
        self.last_trained = datetime.utcnow().isoformat()
        
        return True
