from typing import Dict, Tuple

SEVERITY_KEYWORDS = {
    "high": ["broken","overflow","hazard","dangerous","flood","fell","open manhole","electrical","sewage","slippery","live wire"],
    "medium": ["pothole","garbage","obstruction","stagnant","breeding","blocked","illegal parking"],
    "low": ["streetlight","footpath","debris","outage","dim"]
}

def predict_severity(text: str) -> Tuple[str, Dict[str,int]]:
    t = text.lower()
    score = {"high":0,"medium":0,"low":0}
    for level, kws in SEVERITY_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                score[level] += 1
    best = max(score, key=score.get)
    return (best if score[best] > 0 else "medium", score)
