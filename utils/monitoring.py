"""
Model Monitoring
Tracks model performance and accuracy
"""

from collections import defaultdict
from datetime import datetime

class ModelMonitor:
    def __init__(self):
        self.predictions = defaultdict(list)
        self.feedback = []
        self.total_predictions = 0
    
    def log_prediction(self, analysis: dict):
        """Log a prediction for monitoring"""
        self.predictions[analysis['urgency']].append({
            'timestamp': datetime.utcnow(),
            'confidence': analysis['urgency_confidence'],
            'risk_score': analysis['risk_score']
        })
        self.total_predictions += 1
    
    def log_feedback(self, predicted: str, actual: str):
        """Log feedback for accuracy tracking"""
        self.feedback.append({
            'predicted': predicted,
            'actual': actual,
            'timestamp': datetime.utcnow(),
            'correct': predicted == actual
        })
    
    def get_accuracy(self, model_name: str) -> float:
        """Calculate model accuracy from feedback"""
        if not self.feedback:
            return 0.0
        
        correct = sum(1 for f in self.feedback if f['correct'])
        return round(correct / len(self.feedback), 3)
    
    def get_mae(self, model_name: str) -> float:
        """Get mean absolute error for regression models"""
        # Placeholder - implement based on actual feedback
        return 0.0
    
    def get_total_predictions(self) -> int:
        return self.total_predictions
    
    def get_feedback_count(self) -> int:
        return len(self.feedback)
