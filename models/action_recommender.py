"""
Action Recommender
Recommends actions and NGO types based on case analysis
"""

class ActionRecommender:
    def __init__(self):
        self.version = "1.0.0"
    
    def recommend(self, description: str, urgency: str, incident_type: str, entities: dict) -> dict:
        """Generate recommended actions and NGO types"""
        actions = []
        action_plan = []
        ngo_types = []
        
        # Urgency-based actions
        if urgency == 'critical':
            actions.append('Contact survivor immediately within 1 hour')
            actions.append('Ensure immediate safety - coordinate emergency shelter if needed')
            actions.append('Alert emergency response team')
            action_plan.extend([
                '1. Immediate safety assessment call',
                '2. Coordinate emergency shelter/safe house',
                '3. Medical evaluation if needed',
                '4. Document all interactions',
                '5. Schedule 24-hour follow-up'
            ])
        elif urgency == 'high':
            actions.append('Schedule contact within 24 hours')
            actions.append('Assess safety situation and provide resources')
            action_plan.extend([
                '1. Contact within 24 hours',
                '2. Safety planning session',
                '3. Provide emergency contacts',
                '4. Schedule 48-hour follow-up'
            ])
        else:
            actions.append('Schedule follow-up within 3-5 days')
            actions.append('Provide support resources and hotline information')
            action_plan.extend([
                '1. Initial contact within 5 days',
                '2. Needs assessment',
                '3. Resource referrals',
                '4. Weekly follow-ups'
            ])
        
        # Medical indicators
        if entities.get('medical_indicators'):
            actions.append('Coordinate medical examination and treatment')
            ngo_types.append('Medical Services')
        
        # Legal indicators
        if entities.get('legal_indicators'):
            actions.append('Refer to legal aid services')
            ngo_types.append('Legal Aid')
        
        # Psychological support
        if entities.get('psychological_state') in ['Severe Distress', 'High Anxiety', 'Depression']:
            actions.append('Prioritize mental health counseling referral')
            ngo_types.append('Mental Health Services')
        
        # Incident type specific
        incident_lower = incident_type.lower()
        if 'domestic' in incident_lower or 'gbv' in incident_lower:
            ngo_types.extend(['GBV Support', 'Shelter Services'])
            actions.append('Provide domestic violence resources and safety planning')
        
        if 'child' in incident_lower or (entities.get('victim_age') and entities['victim_age'] < 18):
            ngo_types.append('Child Protection Services')
            actions.append('Report to child protection authorities')
        
        if 'fgm' in incident_lower:
            ngo_types.append('FGM Prevention')
            actions.append('Connect with FGM prevention and support organizations')
        
        if 'trafficking' in incident_lower or 'labor' in incident_lower:
            ngo_types.append('Anti-Trafficking')
            actions.append('Coordinate with anti-trafficking organizations')
        
        # Default NGO types
        if not ngo_types:
            ngo_types = ['General Support Services', 'Crisis Intervention']
        
        return {
            'actions': actions[:5],  # Top 5 actions
            'action_plan': action_plan,
            'ngo_types': list(set(ngo_types))  # Remove duplicates
        }
    
    def is_loaded(self) -> bool:
        return True
