import re
from functools import lru_cache

TOKEN_PATTERN = re.compile(r'\w+')
ASSERTIVE_VERBS = {"is", "are", "must", "should", "cannot", "prove", "proves"}
MODALS = {"always", "never", "only", "necessarily", "impossible", "obviously"}
DEPTH_TRIGGERS = {"because", "since", "therefore", "implies", "means", "consequently"}
TENSION_ANCHORS = ["You are wrong", "That is a fallacy", "Evidence contradicts", "I disagree"]

class SemanticTensionSensor:
    @classmethod
    @lru_cache(maxsize=1)
    def get_sensor(cls):
        try:
            from sentence_transformers import SentenceTransformer
            # Fast, quantized CPU model
            model = SentenceTransformer('all-MiniLM-L6-v2')
            anchors_emb = model.encode(TENSION_ANCHORS, convert_to_tensor=True)
            return model, anchors_emb
        except Exception:
            return None, None

    @classmethod
    def measure(cls, text: str) -> float:
        model, anchors = cls.get_sensor()
        if model is None or len(text) < 10: return 0.0
        
        try:
            from sentence_transformers import util
            emb = model.encode(text, convert_to_tensor=True)
            scores = util.cos_sim(emb, anchors)
            # Scale max similarity (0.3 is high here) to 0-10
            return min(max(0, (float(scores.max()) - 0.2) * 25), 10.0)
        except:
            return 0.0

def estimate_debate_pressure(text: str, rebuttal_timer: float) -> float:
    # 1. Regex Density
    tokens = TOKEN_PATTERN.findall(text.lower())
    density = sum(1 for t in tokens if t in ASSERTIVE_VERBS or t in MODALS)
    if tokens: density /= (len(tokens) / 10) # Normalization
    
    # 2. Semantic Spike
    tension = SemanticTensionSensor.measure(text)
    
    # 3. Time Urgency
    urgency = 0.0
    if rebuttal_timer < 10.0:
        urgency = (10.0 - rebuttal_timer) * 0.5
        
    return min(density + tension + urgency, 10.0)