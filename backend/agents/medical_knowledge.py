
import faiss
import numpy as np
import os
from utils.llm_service import llm_service

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

class MedicalKnowledgeAgent:
    def __init__(self):
        # Expanded knowledge base
        self.documents = [
            "Hypertension (High BP): Guidelines suggest reducing sodium to <2.3g/day, increasing potassium, and Aerobic exercise 90-150 min/week.",
            "Type 2 Diabetes Prevention: Weight loss of 7% of body weight, 150 min/week of moderate activity, Metformin consideration for high risk.",
            "Cholesterol Management: Reduce saturated fats to <7% of calories, eliminate trans fats, increase soluble fiber (10-25g/day).",
            "General Wellness: 7-9 hours of sleep, hydration (2-3L/day), moderation in alcohol intake, avoidance of tobacco products.",
            "Obesity Management: Caloric restricted diet, behavioral therapy, detailed food logging, increase NEAT (Non-Exercise Activity Thermogenesis).",
            "Stress & Mental Health: Mindfulness meditation, cognitive behavioral techniques, adequate social support systems reduce cardiovascular risk."
        ]
        self.index = None
        self.model = None
        self._initialize_rag()

    def _initialize_rag(self):
        if SentenceTransformer:
            try:
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                embeddings = self.model.encode(self.documents)
                dimension = embeddings.shape[1]
                self.index = faiss.IndexFlatL2(dimension)
                self.index.add(np.array(embeddings).astype('float32'))
            except Exception as e:
                import traceback
                traceback.print_exc()
                print(f"Failed to load RAG model: {e}")
                self.model = None
        else:
             print("SentenceTransformer not imported. RAG disabled.")

    def retrieve_guidelines(self, risk_level, user_context=None):
        if not self.model or not self.index:
            return ["RAG System Unavailable - Using default safe guidelines."]

        # 1. Retrieval
        query = f"Preventive guidelines for {risk_level} risk {user_context or ''}"
        query_vector = self.model.encode([query])
        k = 3
        D, I = self.index.search(np.array(query_vector).astype('float32'), k)
        retrieved_docs = [self.documents[i] for i in I[0]]
        
        # 2. LLM Synthesis
        prompt = f"""
        You are a Medical Knowledge Agent.
        
        User Context: {user_context or 'General User'} at {risk_level} Risk.
        Retrieved Medical Guidelines:
        {chr(10).join(['- ' + d for d in retrieved_docs])}
        
        Task:
        Interpret these guidelines specifically for the user. Adapt the advice to be relevant to their condition.
        Constraints: No diagnosis, No medication prescription. Focus on lifestyle and prevention.
        
        Output:
        Concise, contextualized list of preventive actions.
        """
        
        contextualized_advice = llm_service.generate_response(prompt)
        
        # Return structured if possible, but for now we return the LLM text as the "guideline"
        # The frontend expects a list, so we might try to split it or just return a list with one big string
        return [contextualized_advice] 
