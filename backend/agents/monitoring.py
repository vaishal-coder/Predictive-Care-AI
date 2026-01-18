import numpy as np

class MonitoringAgent:
    def __init__(self):
        pass

    def check_trends(self, current_data, history):
        """
        current_data: dict
        history: list of dicts
        """
        alerts = []
        if not history:
            return "No historical data to compare."

        # Simple trend analysis
        last_record = history[-1]
        
        if current_data['bp'] > last_record.get('bp', 0) + 10:
             alerts.append("ALERT: Significant rise in Blood Pressure detected.")
        
        if current_data['sugar'] > last_record.get('sugar', 0) + 20:
             alerts.append("ALERT: Spike in Sugar levels detected.")
             
        if not alerts:
            return "Health trends are stable."
        
        return "\n".join(alerts)
