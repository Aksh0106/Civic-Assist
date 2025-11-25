import joblib, numpy as np
from typing import Dict, Any, Tuple, List
from agent.utils import clean_text, ensure_min_length
from agent.severity import predict_severity
from agent.rules import RECOMMENDED_STEPS, DEFAULT_STEPS, DEPARTMENT_CONTACT_HINTS
from agent.memory import generate_id, log_interaction, count_similar

class CitizenIssueAgent:
    def __init__(self,
                 dept_model_path: str = "models/department_model.pkl",
                 cat_model_path: str = "models/category_model.pkl"):
        self.dept_model = joblib.load(dept_model_path)
        self.cat_model = joblib.load(cat_model_path)

    def _predict_with_conf(self, model, text: str) -> Tuple[str, float]:
        probs = model.predict_proba([text])[0]
        classes = model.classes_
        i = int(np.argmax(probs))
        return classes[i], float(probs[i])

    def _timeline_by_severity(self, severity: str) -> Dict[str,str]:
        if severity == "high":
            return {"initial":"0–4 hours","follow_up":"1–2 days","closure":"3–7 days"}
        elif severity == "medium":
            return {"initial":"24 hours","follow_up":"3–5 days","closure":"7–14 days"}
        return {"initial":"2–3 days","follow_up":"7–10 days","closure":"14–21 days"}

    def _escalation_by_severity(self, severity: str) -> str:
        if severity == "high":
            return "Escalate to emergency unit if no response within 2 hours."
        elif severity == "medium":
            return "Escalate to supervisor if no response within 48 hours."
        return "Escalate if no response within 5 days."

    def run(self, text: str) -> Dict[str,Any]:
        incoming = clean_text(text)
        ensure_min_length(incoming)

        dept, dept_conf = self._predict_with_conf(self.dept_model, incoming)
        cat, cat_conf = self._predict_with_conf(self.cat_model, incoming)
        sev, sev_scores = predict_severity(incoming)
        steps = RECOMMENDED_STEPS.get(cat, DEFAULT_STEPS)
        contacts = DEPARTMENT_CONTACT_HINTS.get(dept, ["General helpline","Ward office"])

        complaint_id = generate_id()
        status = "Pending"
        similar_reports = count_similar(incoming, cat)

        plan = {
            "complaint_id": complaint_id,
            "status": status,
            "similar_reports": similar_reports,
            "summary": incoming,
            "department": {"label": dept, "confidence": round(dept_conf, 3)},
            "category": {"label": cat, "confidence": round(cat_conf, 3)},
            "severity": {"label": sev, "evidence": sev_scores},
            "recommended_steps": steps,
            "timeline": self._timeline_by_severity(sev),
            "contacts": contacts,
            "escalation": self._escalation_by_severity(sev),
            "citizen_checklist": [
                "Confirm ticket ID/receipt of complaint.",
                "Share evidence and exact location/landmark.",
                "Request interim safety measures if risk exists.",
                "Escalate per timeline if unresolved."
            ]
        }

        log_interaction({
            "id": complaint_id,
            "timestamp": __import__("time").strftime("%Y-%m-%d %H:%M:%S"),
            "text": incoming,
            "department": dept,
            "category": cat,
            "severity": sev,
            "status": status,
            "confidence": {"department": dept_conf, "category": cat_conf},
            "severity_evidence": sev_scores
        })

        return plan
