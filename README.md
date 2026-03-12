# SafeVoice AI Service

Production-grade ML pipeline for GBV case analysis and management.

## 🎯 Features

### Core ML Models
- **Urgency Classifier** - Classifies cases as critical/high/medium/low
- **Risk Predictor** - Predicts escalation probability and risk scores
- **Entity Extractor** - Extracts key information (location, timeframe, relationships)
- **Action Recommender** - Suggests actions and appropriate NGO types

### Production Features
- ✅ RESTful API with Flask
- ✅ Model versioning and registry
- ✅ Feedback loop for continuous learning
- ✅ Prometheus metrics for monitoring
- ✅ Automated retraining pipeline
- ✅ PostgreSQL integration for data storage
- ✅ Batch processing support
- ✅ Health checks and status endpoints

## 🚀 Quick Start

### Installation

```bash
cd safevoice-ai-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/safevoice_ai
FLASK_ENV=production
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key  # Optional fallback
```

### Run Service

```bash
# Development
python api/app.py

# Production
gunicorn -w 4 -b 0.0.0.0:5000 api.app:app
```

## 📡 API Endpoints

### Analyze Case
```bash
POST /api/v1/analyze
Content-Type: application/json

{
  "report_id": "uuid",
  "description": "Case description text",
  "incident_type": "GBV",
  "location": "Lagos, Nigeria"
}
```

**Response:**
```json
{
  "urgency": "high",
  "urgency_confidence": 0.85,
  "classification": "Domestic Violence",
  "risk_score": 72.5,
  "escalation_probability": 0.73,
  "immediate_danger": true,
  "medical_attention_needed": true,
  "police_involvement_recommended": false,
  "psychological_state": "High Anxiety",
  "recommended_actions": [
    "Schedule contact within 24 hours",
    "Coordinate medical examination",
    "Provide emergency contacts"
  ],
  "action_plan": [...],
  "recommended_ngo_types": ["GBV Support", "Medical Services"],
  "model_version": {...}
}
```

### Submit Feedback
```bash
POST /api/v1/feedback

{
  "report_id": "uuid",
  "predicted_urgency": "high",
  "actual_urgency": "critical",
  "feedback_type": "correction"
}
```

### Trigger Retraining
```bash
POST /api/v1/retrain
Authorization: Bearer <admin-token>
```

### Model Status
```bash
GET /api/v1/models/status
```

### Health Check
```bash
GET /health
```

## 🔄 Training Pipeline

### Manual Training
```bash
python training/pipeline.py
```

### Automated Training
- Triggers automatically when feedback threshold is reached
- Scheduled retraining (weekly/monthly)
- A/B testing for model versions

## 🏗️ Architecture

```
┌─────────────┐
│  NestJS API │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────┐
│  Flask AI API   │
├─────────────────┤
│ • Urgency Model │
│ • Risk Model    │
│ • Entity NER    │
│ • Recommender   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌──────┐  ┌──────┐
│ PG DB│  │Redis │
└──────┘  └──────┘
```

## 📊 Model Performance

Current metrics (will improve with training data):

| Model | Metric | Score |
|-------|--------|-------|
| Urgency Classifier | Accuracy | TBD |
| Risk Predictor | MAE | TBD |
| Entity Extractor | F1 Score | TBD |

## 🔐 Security

- API authentication with JWT
- Rate limiting
- Input validation
- SQL injection protection
- CORS configuration

## 📈 Monitoring

- Prometheus metrics at `/metrics`
- Model accuracy tracking
- Prediction distribution
- Response time monitoring

## 🧪 Testing

```bash
pytest tests/
```

## 🚢 Deployment

### Docker
```bash
docker build -t safevoice-ai .
docker run -p 5000:5000 safevoice-ai
```

### Render/Railway
- Connect GitHub repo
- Set environment variables
- Deploy automatically

## 🎓 Training Data

Models improve with:
- NGO feedback on urgency classifications
- Actual case outcomes
- Resolution times
- Escalation events

## 📝 License

MIT

## 🤝 Contributing

See CONTRIBUTING.md

---

**Built with ❤️ for SafeVoice**
