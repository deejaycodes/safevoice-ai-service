"""
Spam Detector
Filters out spam, test messages, and irrelevant content
"""

class SpamDetector:
    def __init__(self):
        self.version = "1.0.0"
        
        # Spam indicators
        self.spam_keywords = [
            'test', 'testing', 'hello', 'hi there', 'sample',
            'pizza', 'ice cream', 'weather', 'favorite color',
            'lorem ipsum', 'asdf', 'qwerty', '123456'
        ]
        
        # Violence/crisis keywords (legitimate reports)
        self.legitimate_keywords = [
            'abuse', 'violence', 'assault', 'rape', 'beat', 'hit',
            'hurt', 'pain', 'scared', 'afraid', 'help', 'emergency',
            'threatened', 'weapon', 'knife', 'gun', 'bleeding',
            'injured', 'hospital', 'police', 'escape', 'hiding'
        ]
    
    def is_spam(self, description: str) -> dict:
        """
        Detect if report is spam
        
        Returns:
        {
            'is_spam': bool,
            'confidence': float,
            'reason': str
        }
        """
        description_lower = description.lower().strip()
        
        # Check 1: Too short (less than 20 characters)
        if len(description_lower) < 20:
            return {
                'is_spam': True,
                'confidence': 0.95,
                'reason': 'Description too short'
            }
        
        # Check 2: Contains spam keywords
        spam_count = sum(1 for keyword in self.spam_keywords if keyword in description_lower)
        if spam_count >= 2:
            return {
                'is_spam': True,
                'confidence': 0.90,
                'reason': f'Contains {spam_count} spam indicators'
            }
        
        # Check 3: No legitimate crisis keywords
        legitimate_count = sum(1 for keyword in self.legitimate_keywords if keyword in description_lower)
        
        if legitimate_count == 0 and spam_count >= 1:
            return {
                'is_spam': True,
                'confidence': 0.85,
                'reason': 'No crisis indicators found'
            }
        
        # Check 4: Repeated characters (e.g., "aaaaaaa", "hahahaha")
        if self._has_repeated_chars(description_lower):
            return {
                'is_spam': True,
                'confidence': 0.80,
                'reason': 'Repeated characters detected'
            }
        
        # Check 5: Too many numbers (likely test data)
        digit_ratio = sum(c.isdigit() for c in description) / len(description)
        if digit_ratio > 0.3:
            return {
                'is_spam': True,
                'confidence': 0.75,
                'reason': 'Too many numbers'
            }
        
        # Legitimate report
        return {
            'is_spam': False,
            'confidence': 0.90 if legitimate_count >= 2 else 0.70,
            'reason': 'Appears legitimate'
        }
    
    def _has_repeated_chars(self, text: str) -> bool:
        """Check for repeated characters (spam pattern)"""
        import re
        # Match 5+ repeated characters
        pattern = r'(.)\1{4,}'
        return bool(re.search(pattern, text))
    
    def is_loaded(self) -> bool:
        return True
