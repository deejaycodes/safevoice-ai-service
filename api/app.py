"""
SafeVoice AI Service - Main API
Production-grade ML pipeline for GBV case analysis
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
from prometheus_client import Counter, Histogram, generate_latest
import time

from models.urgency_classifier import UrgencyClassifier
from models.risk_predictor import RiskPredictor
from models.entity_extractor import EntityExtractor
from models.action_recommender import ActionRecommender
from utils.database import DatabaseConnector
from utils.monitoring import ModelMonitor

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('ai_requests_total', 'Total AI analysis requests', ['endpoint', 'status'])
REQUEST_DURATION = Histogram('ai_request_duration_seconds', 'Request duration', ['endpoint'])
MODEL_PREDICTIONS = Counter('model_predictions_total', 'Total predictions', ['model', 'prediction'])

# Initialize ML models
urgency_classifier = UrgencyClassifier()
risk_predictor = RiskPredictor()
entity_extractor = EntityExtractor()
action_recommender = ActionRecommender()
db = DatabaseConnector()
monitor = ModelMonitor()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'models_loaded': {
            'urgency_classifier': urgency_classifier.is_loaded(),
            'risk_predictor': risk_predictor.is_loaded(),
            'entity_extractor': entity_extractor.is_loaded(),
            'action_recommender': action_recommender.is_loaded()
        }
    }), 200

@app.route('/api/v1/analyze', methods=['POST'])
def analyze_case():
    """
    Main endpoint for case analysis
    
    Request body:
    {
        "report_id": "uuid",
        "description": "text",
        "incident_type": "string",
        "location": "string",
        "metadata": {}
    }
    """
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        # Validate input
        if not data.get('description'):
            REQUEST_COUNT.labels(endpoint='analyze', status='error').inc()
            return jsonify({'error': 'Description is required'}), 400
        
        description = data['description']
        incident_type = data.get('incident_type', 'unknown')
        location = data.get('location', '')
        report_id = data.get('report_id')
        
        logger.info(f"Analyzing case: {report_id}")
        
        # Run ML pipeline
        urgency_result = urgency_classifier.predict(description, incident_type)
        risk_result = risk_predictor.predict(description, urgency_result['urgency'])
        entities = entity_extractor.extract(description, location)
        actions = action_recommender.recommend(
            description, 
            urgency_result['urgency'],
            incident_type,
            entities
        )
        
        # Compile analysis
        analysis = {
            'report_id': report_id,
            'urgency': urgency_result['urgency'],
            'urgency_confidence': urgency_result['confidence'],
            'classification': urgency_result['classification'],
            'risk_score': risk_result['risk_score'],
            'escalation_probability': risk_result['escalation_probability'],
            'immediate_danger': risk_result['immediate_danger'],
            'medical_attention_needed': entities.get('medical_indicators', False),
            'police_involvement_recommended': entities.get('legal_indicators', False),
            'psychological_state': entities.get('psychological_state'),
            'extracted_entities': entities,
            'recommended_actions': actions['actions'],
            'action_plan': actions['action_plan'],
            'recommended_ngo_types': actions['ngo_types'],
            'model_version': {
                'urgency': urgency_classifier.version,
                'risk': risk_predictor.version,
                'entities': entity_extractor.version,
                'actions': action_recommender.version
            },
            'analyzed_at': datetime.utcnow().isoformat()
        }
        
        # Log prediction for monitoring
        MODEL_PREDICTIONS.labels(model='urgency', prediction=urgency_result['urgency']).inc()
        
        # Store analysis for training
        if report_id:
            db.store_analysis(report_id, analysis)
        
        # Monitor model performance
        monitor.log_prediction(analysis)
        
        duration = time.time() - start_time
        REQUEST_DURATION.labels(endpoint='analyze').observe(duration)
        REQUEST_COUNT.labels(endpoint='analyze', status='success').inc()
        
        logger.info(f"Analysis complete for {report_id} in {duration:.2f}s")
        
        return jsonify(analysis), 200
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        REQUEST_COUNT.labels(endpoint='analyze', status='error').inc()
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.route('/api/v1/batch-analyze', methods=['POST'])
def batch_analyze():
    """Batch analysis for multiple cases"""
    try:
        data = request.get_json()
        cases = data.get('cases', [])
        
        if not cases:
            return jsonify({'error': 'No cases provided'}), 400
        
        results = []
        for case in cases:
            # Reuse analyze logic
            result = analyze_case_internal(case)
            results.append(result)
        
        return jsonify({'results': results, 'count': len(results)}), 200
        
    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback for model improvement
    
    Request body:
    {
        "report_id": "uuid",
        "predicted_urgency": "high",
        "actual_urgency": "critical",
        "feedback_type": "correction|validation",
        "notes": "optional"
    }
    """
    try:
        data = request.get_json()
        
        report_id = data.get('report_id')
        predicted = data.get('predicted_urgency')
        actual = data.get('actual_urgency')
        
        if not all([report_id, predicted, actual]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store feedback for retraining
        db.store_feedback(data)
        
        # Update model monitoring
        monitor.log_feedback(predicted, actual)
        
        logger.info(f"Feedback received for {report_id}: {predicted} -> {actual}")
        
        return jsonify({'message': 'Feedback recorded', 'report_id': report_id}), 200
        
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/retrain', methods=['POST'])
def trigger_retraining():
    """Trigger model retraining (admin only)"""
    try:
        # TODO: Add authentication
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Trigger async retraining job
        from training.pipeline import trigger_training
        job_id = trigger_training()
        
        return jsonify({
            'message': 'Retraining triggered',
            'job_id': job_id
        }), 202
        
    except Exception as e:
        logger.error(f"Retraining error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/v1/models/status', methods=['GET'])
def model_status():
    """Get model versions and performance metrics"""
    try:
        status = {
            'models': {
                'urgency_classifier': {
                    'version': urgency_classifier.version,
                    'accuracy': monitor.get_accuracy('urgency'),
                    'last_trained': urgency_classifier.last_trained
                },
                'risk_predictor': {
                    'version': risk_predictor.version,
                    'mae': monitor.get_mae('risk'),
                    'last_trained': risk_predictor.last_trained
                }
            },
            'total_predictions': monitor.get_total_predictions(),
            'feedback_count': monitor.get_feedback_count()
        }
        
        return jsonify(status), 200
        
    except Exception as e:
        logger.error(f"Status error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/metrics', methods=['GET'])
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

def analyze_case_internal(case_data):
    """Internal helper for batch processing"""
    # Simplified version of analyze_case
    description = case_data['description']
    urgency = urgency_classifier.predict(description, case_data.get('incident_type', 'unknown'))
    return {
        'report_id': case_data.get('report_id'),
        'urgency': urgency['urgency'],
        'confidence': urgency['confidence']
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
