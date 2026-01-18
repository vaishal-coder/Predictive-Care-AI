
from utils.llm_service import llm_service

class RecommendationAgent:
    def __init__(self):
        pass

    def generate_recommendation(self, user_data, risk_result, guidelines):
        """
        Uses LLM to generate the final personalized plan.
        """
        risk_level = risk_result.get('risk_level', 'Unknown')
        risk_explanation = risk_result.get('explanation', '')
        
        # Guidelines is now a list containing the LLM synthesized advice
        guidelines_text = "\n".join(guidelines)
        
        prompt = f"""
        You are a Preventive Care Recommendation Agent.
        
        Inputs:
        1. User Profile: {user_data}
        2. Risk Analysis: {risk_level} Risk. {risk_explanation}
        3. Medical Guidelines (Contextualized): {guidelines_text}
        
        Task:
        Generate a strictly structured Personal Preventive Care Plan.
        The tone must be professional, empathetic, and motivating.
        
        Structure your response exactly as follows:
        
        **Risk Summary**
        [Brief summary of why they are at this risk level]
        
        **Immediate Actions**
        [Bulleted list of high-priority changes]
        
        **Long-term Lifestyle Goals**
        [Sustainable habit changes]
        
        **Monitoring Plan**
        [What to track and when to see a doctor]
        
        """
        
        final_plan = llm_service.generate_response(prompt)
        return final_plan
