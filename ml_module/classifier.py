"""
AI/NLP Module for Automatic Complaint Classification
Uses TF-IDF vectorization and Naive Bayes classifier
"""
import os
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib


# Category definitions with keywords for fallback
CATEGORY_KEYWORDS = {
    'Electricity': [
        'electricity', 'power', 'light', 'electric', 'voltage', 'transformer',
        'pole', 'wire', 'current', 'blackout', 'outage', 'meter', 'bill',
        'street light', 'lamp', 'bulb', 'connection', 'shock'
    ],
    'Water Supply': [
        'water', 'supply', 'pipe', 'leak', 'drainage', 'sewage', 'tap',
        'pipeline', 'drinking water', 'tank', 'bore', 'pump', 'pressure',
        'contaminated', 'dirty', 'overflow', 'blockage', 'clog'
    ],
    'Road & Transport': [
        'road', 'street', 'pothole', 'traffic', 'signal', 'transport',
        'footpath', 'pavement', 'crossing', 'highway', 'pathway', 'jam',
        'congestion', 'sign', 'divider', 'crack', 'damage', 'repair'
    ],
    'Cleanliness': [
        'garbage', 'waste', 'trash', 'dirty', 'cleanliness', 'dustbin',
        'sanitation', 'litter', 'dump', 'smell', 'hygiene', 'sweeping',
        'cleaning', 'stink', 'odor', 'filth', 'rubble', 'debris'
    ],
    'Noise': [
        'noise', 'sound', 'loud', 'disturbance', 'Speaker', 'music',
        'construction', 'pollution', 'volume', 'shouting', 'party',
        'horn', 'siren', 'barking', 'disturb', 'quiet'
    ],
    'Other': [
        'other', 'miscellaneous', 'general', 'complaint', 'issue', 'problem'
    ]
}


# Training data for the ML model
TRAINING_DATA = {
    'Electricity': [
        "There is no street light in our area for the past week",
        "Power outage happening daily since last month",
        "Electric pole wire is broken and hanging dangerously",
        "Transformer is making buzzing noise and sparking",
        "Street lights not working at night causing safety issues",
        "High electricity bill despite low usage",
        "Voltage fluctuation damaging home appliances",
        "Electric meter is faulty and needs replacement",
        "No power supply for 3 days in our locality",
        "Damaged electric wire near children's park"
    ],
    'Water Supply': [
        "No water supply for past 3 days in our area",
        "Water pipeline is leaking on the main road",
        "Dirty contaminated water coming from taps",
        "Drainage overflow causing health hazard",
        "Water pressure is very low cannot fill tanks",
        "Sewage blockage in our street smelling bad",
        "Broken water pipe wasting water",
        "No drinking water facility in the area",
        "Water tank is overflowing for days",
        "Underground water leakage damaging road"
    ],
    'Road & Transport': [
        "Large pothole on main road causing accidents",
        "Traffic signal not working at busy intersection",
        "Road is completely damaged needs urgent repair",
        "Footpath is broken elderly people falling",
        "Missing road signs causing confusion",
        "Heavy traffic jam every morning",
        "Zebra crossing paint has faded not visible",
        "Speed breaker is too high damaging vehicles",
        "Road divider is broken dangerous for drivers",
        "Street has multiple cracks needs resurfacing"
    ],
    'Cleanliness': [
        "Garbage not collected for a week piling up",
        "Dustbins are overflowing attracting flies",
        "People dumping waste on roadside",
        "Bad smell from garbage near residential area",
        "No waste collection in our locality",
        "Stray animals spreading garbage everywhere",
        "Open drain is full of trash causing blockage",
        "Construction debris dumped on road",
        "Littering problem in public park",
        "Sanitation workers not cleaning streets"
    ],
    'Noise': [
        "Loud music from neighbor every night",
        "Construction noise starting at 6 AM daily",
        "DJ sound system disturbing whole colony",
        "Factory noise pollution throughout day",
        "Barking dogs not letting us sleep",
        "Party noise till late night",
        "Horn honking near hospital zone",
        "Loud speaker announcements disturbing studies",
        "Noisy generator running all night",
        "Vehicle modification causing loud sound"
    ],
    'Other': [
        "General inquiry about municipal services",
        "Request for information",
        "Feedback on recent improvements",
        "Suggestion for area development",
        "Appreciation for good work",
        "Question about upcoming projects",
        "Request for new facility",
        "Complaint about undefined issue",
        "General grievance redressal",
        "Miscellaneous concern"
    ]
}


class ComplaintClassifier:
    """
    Complaint classifier using TF-IDF + Naive Bayes
    Falls back to keyword matching if confidence is low
    """
    
    def __init__(self, model_path=None):
        """Initialize classifier and load model if exists"""
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), 'complaint_classifier.pkl'
        )
        self.model = None
        self.categories = list(CATEGORY_KEYWORDS.keys())
        
        # Try to load existing model
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            self.train()
    
    def preprocess_text(self, text):
        """Clean and preprocess text for classification"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def train(self):
        """Train the classifier on predefined training data"""
        # Prepare training data
        X_train = []
        y_train = []
        
        for category, texts in TRAINING_DATA.items():
            for text in texts:
                X_train.append(self.preprocess_text(text))
                y_train.append(category)
        
        # Create pipeline with TF-IDF and Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=500,
                ngram_range=(1, 2),  # Use unigrams and bigrams
                stop_words='english'
            )),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Save the trained model
        self.save_model()
        print(f"✓ Model trained successfully with {len(X_train)} samples")
    
    def save_model(self):
        """Save trained model to disk"""
        try:
            joblib.dump(self.model, self.model_path)
            print(f"✓ Model saved to {self.model_path}")
        except Exception as e:
            print(f"✗ Error saving model: {e}")
    
    def load_model(self):
        """Load trained model from disk"""
        try:
            self.model = joblib.load(self.model_path)
            print(f"✓ Model loaded from {self.model_path}")
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            self.train()
    
    def keyword_based_classification(self, text):
        """Fallback keyword-based classification"""
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            scores[category] = score
        
        # Return category with highest score
        max_category = max(scores, key=scores.get)
        if scores[max_category] > 0:
            return max_category
        return 'Other'
    
    def predict(self, text, use_keywords_fallback=True):
        """
        Predict category for given complaint text
        Returns: (category_name, confidence_score)
        """
        if not text or len(text.strip()) < 10:
            return ('Other', 0.5)
        
        # Preprocess
        processed_text = self.preprocess_text(text)
        
        try:
            # Get prediction probabilities
            prediction = self.model.predict([processed_text])[0]
            probabilities = self.model.predict_proba([processed_text])[0]
            confidence = max(probabilities)
            
            # If confidence is low, use keyword fallback
            if use_keywords_fallback and confidence < 0.4:
                keyword_prediction = self.keyword_based_classification(text)
                return (keyword_prediction, 0.6)
            
            return (prediction, confidence)
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            # Fallback to keyword-based
            return (self.keyword_based_classification(text), 0.5)


# Global classifier instance
_classifier = None


def get_classifier():
    """Get or create global classifier instance"""
    global _classifier
    if _classifier is None:
        _classifier = ComplaintClassifier()
    return _classifier


def predict_category(complaint_text):
    """
    Main function to predict complaint category
    Used by Django views
    
    Args:
        complaint_text: The complaint description text
    
    Returns:
        tuple: (category_name, confidence_score)
    """
    classifier = get_classifier()
    return classifier.predict(complaint_text)


# Test function
if __name__ == "__main__":
    # Test the classifier
    test_cases = [
        "There is no street light in our area",
        "Water pipeline is leaking badly",
        "Pothole on main road causing accidents",
        "Garbage not collected for days",
        "Loud noise from construction site",
        "Need information about services"
    ]
    
    print("\n" + "="*60)
    print("TESTING COMPLAINT CLASSIFIER")
    print("="*60 + "\n")
    
    classifier = get_classifier()
    
    for text in test_cases:
        category, confidence = predict_category(text)
        print(f"Text: {text}")
        print(f"Predicted: {category} (Confidence: {confidence:.2%})")
        print("-" * 60)
