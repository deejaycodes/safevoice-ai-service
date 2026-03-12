"""
Database Connector
Handles connections to PostgreSQL for storing analysis and feedback
"""

import os
from sqlalchemy import create_engine, Column, String, JSON, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Analysis(Base):
    __tablename__ = 'ai_analysis'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(String, index=True)
    urgency = Column(String)
    urgency_confidence = Column(Float)
    risk_score = Column(Float)
    escalation_probability = Column(Float)
    analysis_data = Column(JSON)
    model_version = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'ai_feedback'
    
    id = Column(Integer, primary_key=True)
    report_id = Column(String, index=True)
    predicted_urgency = Column(String)
    actual_urgency = Column(String)
    feedback_type = Column(String)
    notes = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseConnector:
    def __init__(self):
        db_url = os.getenv('DATABASE_URL', 'postgresql://localhost/safevoice_ai')
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def store_analysis(self, report_id: str, analysis: dict):
        """Store AI analysis results"""
        try:
            record = Analysis(
                report_id=report_id,
                urgency=analysis['urgency'],
                urgency_confidence=analysis['urgency_confidence'],
                risk_score=analysis['risk_score'],
                escalation_probability=analysis['escalation_probability'],
                analysis_data=analysis,
                model_version=analysis['model_version']
            )
            self.session.add(record)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error storing analysis: {e}")
            return False
    
    def store_feedback(self, feedback: dict):
        """Store feedback for model improvement"""
        try:
            record = Feedback(
                report_id=feedback['report_id'],
                predicted_urgency=feedback['predicted_urgency'],
                actual_urgency=feedback['actual_urgency'],
                feedback_type=feedback.get('feedback_type', 'correction'),
                notes=feedback.get('notes', '')
            )
            self.session.add(record)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error storing feedback: {e}")
            return False
    
    def get_training_data(self):
        """Retrieve data for model training"""
        try:
            # Get all feedback with actual labels
            feedback_records = self.session.query(Feedback).all()
            return feedback_records
        except Exception as e:
            print(f"Error retrieving training data: {e}")
            return []
