#!/usr/bin/env python3
"""
Quick test of the AI service
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.urgency_classifier import UrgencyClassifier
from models.risk_predictor import RiskPredictor
from models.entity_extractor import EntityExtractor
from models.action_recommender import ActionRecommender

def test_pipeline():
    print("=== SafeVoice AI Service Test ===\n")
    
    # Test case
    test_description = """
    My husband beat me last night. He was drunk and hit me multiple times.
    I'm scared and have bruises on my arms. This has happened before.
    I don't know what to do. I'm afraid he will hurt me again.
    """
    
    print("Test Case Description:")
    print(test_description)
    print("\n" + "="*50 + "\n")
    
    # Initialize models
    print("Loading models...")
    urgency_classifier = UrgencyClassifier()
    risk_predictor = RiskPredictor()
    entity_extractor = EntityExtractor()
    action_recommender = ActionRecommender()
    print("✅ All models loaded\n")
    
    # Run analysis
    print("Running analysis...\n")
    
    urgency_result = urgency_classifier.predict(test_description, "Domestic Violence")
    print(f"📊 Urgency: {urgency_result['urgency'].upper()}")
    print(f"   Confidence: {urgency_result['confidence']:.2f}")
    print(f"   Classification: {urgency_result['classification']}\n")
    
    risk_result = risk_predictor.predict(test_description, urgency_result['urgency'])
    print(f"⚠️  Risk Score: {risk_result['risk_score']}/100")
    print(f"   Escalation Probability: {risk_result['escalation_probability']:.2%}")
    print(f"   Immediate Danger: {risk_result['immediate_danger']}\n")
    
    entities = entity_extractor.extract(test_description, "")
    print(f"🔍 Extracted Entities:")
    print(f"   Timeframe: {entities['timeframe']}")
    print(f"   Relationship: {entities['perpetrator_relationship']}")
    print(f"   Medical Indicators: {entities['medical_indicators']}")
    print(f"   Legal Indicators: {entities['legal_indicators']}")
    print(f"   Psychological State: {entities['psychological_state']}\n")
    
    actions = action_recommender.recommend(
        test_description,
        urgency_result['urgency'],
        "Domestic Violence",
        entities
    )
    print(f"💡 Recommended Actions:")
    for i, action in enumerate(actions['actions'], 1):
        print(f"   {i}. {action}")
    
    print(f"\n🏢 Recommended NGO Types:")
    for ngo_type in actions['ngo_types']:
        print(f"   • {ngo_type}")
    
    print(f"\n📋 Action Plan:")
    for step in actions['action_plan']:
        print(f"   {step}")
    
    print("\n" + "="*50)
    print("✅ Test completed successfully!")
    print("\nNext steps:")
    print("1. Run: python api/app.py")
    print("2. Test API: curl http://localhost:5000/health")
    print("3. Integrate with NestJS backend")

if __name__ == '__main__':
    test_pipeline()
