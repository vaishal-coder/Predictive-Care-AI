
from agents.risk_prediction import RiskPredictionAgent
from agents.medical_knowledge import MedicalKnowledgeAgent
from agents.recommendation import RecommendationAgent
from agents.memory import MemoryAgent
from utils.llm_service import llm_service

class OrchestratorAgent:
    def __init__(self):
        print("Initializing High-End Agentic System...")
        self.risk_agent = RiskPredictionAgent()
        self.rag_agent = MedicalKnowledgeAgent()
        self.rec_agent = RecommendationAgent()
        self.memory_agent = MemoryAgent()
        print("Agents Initialized.")

    def process_request(self, user_data, history=None):
        results = {}
        
        # 0. Check History (Memory)
        # In a real system, we'd feed this into the agents.
        past_interactions = self.memory_agent.get_history()
        
        # 1. Risk Identity & Interpretation
        print("Orchestrator: Invoking Risk Agent...")
        risk_result = self.risk_agent.predict_risk(user_data)
        results['risk_analysis'] = risk_result
        
        # 2. Knowledge Retrieval (Contextualized)
        print("Orchestrator: Invoking Medical Knowledge Agent...")
        risk_level = risk_result.get('risk_level', 'Low')
        # Pass user specific context string to RAG
        user_ctx = f"Age: {user_data.get('age')}, BMI: {user_data.get('bmi')}, Condition: {risk_level}"
        guidelines = self.rag_agent.retrieve_guidelines(risk_level, user_context=user_ctx)
        results['guidelines'] = guidelines
        
        # 3. Recommendation Reasoning
        print("Orchestrator: Invoking Recommendation Agent...")
        final_plan = self.rec_agent.generate_recommendation(user_data, risk_result, guidelines)
        results['recommendation'] = final_plan
        
        # 4. Memory Storage
        print("Orchestrator: Storing Interaction in Memory...")
        store_status = self.memory_agent.store_interaction(
            user_data, 
            risk_result.get('risk_level'), 
            final_plan
        )
        print(f"Memory Status: {store_status}")
            
        return results
