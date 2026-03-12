"""
Integration with NestJS Backend
Update your NestJS AI service to call this Flask API
"""

# File: SafeHelpHub/src/basics/ai/ai-analysis.service.ts

/*
Add this method to call the Python AI service:

async analyzeIncidentUrgency(incidentText: string): Promise<IncidentAnalysis> {
  try {
    // Call Python AI service
    const response = await axios.post(
      `${process.env.AI_SERVICE_URL}/api/v1/analyze`,
      {
        description: incidentText,
        incident_type: 'GBV',
        location: ''
      },
      {
        timeout: 10000
      }
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
    // Fallback to OpenAI or simulated response
    return this.simulateAnalysis(incidentText);
  }
}

// Add to .env
AI_SERVICE_URL=http://localhost:5000  # or your deployed URL
*/
