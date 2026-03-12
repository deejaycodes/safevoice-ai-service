"""
Risk Predictor Model
Predicts escalation risk and danger levels
"""

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import os
from datetime import datetime

class RiskPredictor:
    def __init__(self):
        self.version = "1.0.0"
        self.model = None
        self.last_trained = None
        self.load_model()
    
    def load_model(self):
        """Load trained model or initialize new one"""
        model_path = 'models/saved/risk_predictor.joblib'
        
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            self.last_trained = datetime.fromtimestamp(os.path.getmtime(model_path)).isoformat()
        else:
            self.model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            self.last_trained = None
    
    def predict(self, description: str, urgency: str) -> dict:
        """Predict risk score and escalation probability"""
        features = self._extract_risk_features(description, urgency)
        risk_score = self._calculate_risk_score(features, urgency)
        
        return {
            'risk_score': round(risk_score, 2),
            'escalation_probability': round(risk_score / 100.0, 2),
            'immediate_danger': urgency in ['critical', 'high'] and risk_score > 70
        }
    
    def _extract_risk_features(self, description: str, urgency: str) -> dict:
        """Extract risk-related features"""
        description_lower = description.lower()
        
        violence_indicators = ['weapon', 'knife', 'gun', 'hit', 'beat', 'hurt']
        repeat_indicators = ['again', 'always', 'every time', 'repeatedly']
        isolation_indicators = ['alone', 'no one', 'isolated', 'trapped', 'locked']
        threat_indicators = ['threaten', 'kill', 'hurt', 'harm']
        
        return {
            'violence_count': sum(1 for w in violence_indicators if w in description_lower),
            'repeat_count': sum(1 for w in repeat_indicators if w in description_lower),
            'isolation_count': sum(1 for w in isolation_indicators if w in description_lower),
            'threat_count': sum(1 for w in threat_indicators if w in description_lower),
            'urgency_level': {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}.get(urgency, 1)
        }
    
    def _calculate_risk_score(self, features: dict, urgency: str) -> float:
        """Calculate risk score"""
        base_score = {'critical': 85, 'high': 65, 'medium': 40, 'low': 20}.get(urgency, 20)
        
        adjustments = (features['violence_count'] * 5 + 
                      features['repeat_count'] * 4 + 
                      features['isolation_count'] * 3 + 
                      features['threat_count'] * 4)
        
        return min(100, base_score + adjustments)
    
    def is_loaded(self) -> bool:
        return self.model is not None
