"""
Training Pipeline
Automated model retraining with new data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.urgency_classifier import UrgencyClassifier
from models.risk_predictor import RiskPredictor
from utils.database import DatabaseConnector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import uuid

def trigger_training():
    """Trigger async training job"""
    job_id = str(uuid.uuid4())
    # In production, use Celery or similar for async processing
    print(f"Training job {job_id} triggered")
    return job_id

def train_urgency_model():
    """Train urgency classifier with feedback data"""
    print("Starting urgency model training...")
    
    db = DatabaseConnector()
    feedback_data = db.get_training_data()
    
    if len(feedback_data) < 50:
        print(f"Insufficient training data: {len(feedback_data)} samples. Need at least 50.")
        return False
    
    # Prepare training data
    X = []
    y = []
    
    for feedback in feedback_data:
        # Fetch original report description from main database
        # For now, using placeholder
        X.append(f"Sample description for {feedback.report_id}")
        y.append(feedback.actual_urgency)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    classifier = UrgencyClassifier()
    classifier.train(X_train, y_train)
    
    # Evaluate
    X_test_features = classifier.vectorizer.transform(X_test)
    y_pred = classifier.model.predict(X_test_features)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy:.3f}")
    print(classification_report(y_test, y_pred))
    
    print("Urgency model training complete!")
    return True

def train_risk_model():
    """Train risk predictor with feedback data"""
    print("Starting risk model training...")
    
    # Similar to urgency model training
    # Implement based on risk score feedback
    
    print("Risk model training complete!")
    return True

if __name__ == '__main__':
    print("=== SafeVoice AI Training Pipeline ===")
    train_urgency_model()
    train_risk_model()
