
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from utils.llm_service import llm_service

class RiskPredictionAgent:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), '../models/risk_model.pkl')
        self.encoder_path = os.path.join(os.path.dirname(__file__), '../models/le.pkl')
        self.model = None
        self.le = None
        self._load_or_train_model()

    def _load_or_train_model(self):
        # ... (Existing ML Code unchanged for brevity/stability) ...
        # I am re-implementing the load checks to ensure it works
        if os.path.exists(self.model_path) and os.path.exists(self.encoder_path):
            self.model = joblib.load(self.model_path)
            self.le = joblib.load(self.encoder_path)
        else:
            self._train_dummy_model()

    def _train_dummy_model(self):
        # Re-using the same training logic as before
        data = {
            'age': np.random.randint(20, 80, 1000),
            'bmi': np.random.uniform(18, 40, 1000),
            'bp': np.random.randint(90, 180, 1000),
            'sugar': np.random.randint(70, 200, 1000),
            'lifestyle': np.random.choice(['Sedentary', 'Active', 'Moderate'], 1000)
        }
        df = pd.DataFrame(data)
        def get_risk(row):
            score = 0
            if row['age'] > 50: score += 1
            if row['bmi'] > 30: score += 1
            if row['bp'] > 140: score += 1
            if row['sugar'] > 140: score += 1
            if row['lifestyle'] == 'Sedentary': score += 1
            if score <= 1: return 'Low'
            elif score <= 3: return 'Medium'
            else: return 'High'
        df['risk'] = df.apply(get_risk, axis=1)
        self.le_lifestyle = LabelEncoder()
        df['lifestyle_encoded'] = self.le_lifestyle.fit_transform(df['lifestyle'])
        X = df[['age', 'bmi', 'bp', 'sugar', 'lifestyle_encoded']]
        y = df['risk']
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        if not os.path.exists(os.path.dirname(self.model_path)):
            os.makedirs(os.path.dirname(self.model_path))
        joblib.dump(self.model, self.model_path)
        ensembers = {'lifestyle': self.le_lifestyle}
        joblib.dump(ensembers, self.encoder_path)
        self.le = ensembers

    def predict_risk(self, user_data):
        if not self.model:
            self._load_or_train_model()
            
        try:
            # 1. ML Deterministic Prediction
            lifestyle_encoded = self.le['lifestyle'].transform([user_data['lifestyle']])[0]
            input_vector = [[
                user_data['age'],
                user_data['bmi'],
                user_data['bp'],
                user_data['sugar'],
                lifestyle_encoded
            ]]
            prediction = self.model.predict(input_vector)[0]
            
            # 2. LLM Interpretation (Agentic Layer)
            prompt = f"""
            You are a Health Risk Prediction Agent.
            
            Context:
            User Data: Age {user_data['age']}, BMI {user_data['bmi']}, BP {user_data['bp']}, Sugar {user_data['sugar']}, Lifestyle {user_data['lifestyle']}
            ML Model Prediction: {prediction} Risk
            
            Task:
            Interpret this risk level in human-understandable terms. 
            Explain why the ML model predicted {prediction} risk by analyzing the user's vitals.
            
            Constraints:
            - Start directly with the analysis.
            - Use bullet points for key factors.
            - Do NOT include "Risk Category: {prediction}" in your response as the UI already shows a badge.
            - Keep it concise but professional.
            """
            
            explanation_node = llm_service.generate_response(prompt)
            
            # Extract explanation if possible, or just return the full text
            # For robustness, we return the text.
            
            return {
                "risk_level": prediction,
                "explanation": explanation_node,
                "raw_ml_output": prediction
            }
        except Exception as e:
            return {"error": str(e), "risk_level": "Unknown"}
