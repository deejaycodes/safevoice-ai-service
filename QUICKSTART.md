# 🚀 Quick Start Guide

## Test the AI Service (2 minutes)

```bash
cd /Users/deji/safevoice-ai-service

# Run test (no installation needed)
python3 test_service.py
```

**Expected output:** Complete AI analysis of a domestic violence case showing urgency, risk score, extracted entities, and recommended actions.

## Deploy to Production (15 minutes)

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

### 2. Create Database
- Dashboard → New → PostgreSQL
- Name: `safevoice-ai-db`
- Plan: Free (or Starter $7/mo)
- Copy the **Internal Database URL**

### 3. Deploy AI Service
- Dashboard → New → Web Service
- Connect this repo: `safevoice-ai-service`
- Settings:
  - **Name:** `safevoice-ai`
  - **Environment:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn -w 4 -b 0.0.0.0:$PORT api.app:app`
  - **Plan:** Starter ($7/mo)

### 4. Add Environment Variables
```
DATABASE_URL = <paste-internal-database-url>
FLASK_ENV = production
SECRET_KEY = <generate-random-string>
```

### 5. Deploy
- Click "Create Web Service"
- Wait 3-5 minutes for deployment
- Copy your service URL: `https://safevoice-ai-xxxxx.onrender.com`

### 6. Test Deployment
```bash
# Health check
curl https://safevoice-ai-xxxxx.onrender.com/health

# Test analysis
curl -X POST https://safevoice-ai-xxxxx.onrender.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Test case description",
    "incident_type": "GBV",
    "location": "Lagos"
  }'
```

## Integrate with NestJS (10 minutes)

### 1. Add Environment Variable
```bash
cd /Users/deji/SafeHelpHub

# Add to .env
echo "AI_SERVICE_URL=https://safevoice-ai-xxxxx.onrender.com" >> .env
```

### 2. Update AI Service
```typescript
// src/basics/ai/ai-analysis.service.ts

import axios from 'axios';

async analyzeIncidentUrgency(incidentText: string, incidentType: string) {
  try {
    const response = await axios.post(
      `${process.env.AI_SERVICE_URL}/api/v1/analyze`,
      {
        description: incidentText,
        incident_type: incidentType,
        location: ''
      },
      { timeout: 10000 }
    );

    return {
      urgency: response.data.urgency,
      classification: response.data.classification,
      extractedEntities: response.data.extracted_entities,
      recommendedActions: response.data.recommended_actions,
      immediateDanger: response.data.immediate_danger,
      medicalAttentionNeeded: response.data.medical_attention_needed,
      policeInvolvementRecommended: response.data.police_involvement_recommended,
      recommendedNgoTypes: response.data.recommended_ngo_types,
      psychologicalState: response.data.psychological_state,
      actionPlan: response.data.action_plan
    };
  } catch (error) {
    this.logger.error(`AI service error: ${error.message}`);
    return this.simulateAnalysis(incidentText); // Fallback
  }
}
```

### 3. Install Axios (if not already)
```bash
npm install axios
```

### 4. Test Integration
```bash
# Rebuild and deploy
npm run build
git add -A
git commit -m "Integrate Python AI service"
git push origin main
```

### 5. Verify
- Submit a test report through mobile app
- Check NGO portal - should see AI analysis
- Verify urgency, risk score, and recommendations appear

## Monitor Performance

### Check Model Status
```bash
curl https://safevoice-ai-xxxxx.onrender.com/api/v1/models/status
```

### View Metrics
```bash
curl https://safevoice-ai-xxxxx.onrender.com/metrics
```

### Submit Feedback (for training)
```bash
curl -X POST https://safevoice-ai-xxxxx.onrender.com/api/v1/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "report_id": "uuid-here",
    "predicted_urgency": "high",
    "actual_urgency": "critical",
    "feedback_type": "correction"
  }'
```

## Troubleshooting

### Service won't start
- Check Render logs
- Verify DATABASE_URL is set
- Ensure all dependencies in requirements.txt

### Low accuracy
- Normal for first 100 cases (rule-based)
- Collect NGO feedback
- Retrain after 100+ feedbacks

### Slow response times
- Upgrade Render plan (more RAM)
- Add Redis caching
- Enable connection pooling

## Next Steps

1. ✅ Deploy AI service
2. ✅ Integrate with NestJS
3. ⏳ Collect feedback from NGOs
4. ⏳ Retrain models (after 100+ cases)
5. ⏳ Monitor accuracy improvements
6. ⏳ Add advanced features (sentiment analysis, pattern detection)

## Support

- **Technical Docs:** README.md
- **Deployment Guide:** DEPLOYMENT.md
- **Integration Help:** INTEGRATION.md
- **Overview:** EXECUTIVE_SUMMARY.md

---

**Total Time:** ~30 minutes from zero to production 🚀
