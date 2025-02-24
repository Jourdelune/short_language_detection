from .dict_detector import DictDetector

class Detector:
    def __init__(self, reliability_threshold: float = 0.5):
        self._reliability_threshold = reliability_threshold
        self._dict_detector = DictDetector()
        
    def predict(self, text: str) -> str:
        return self._dict_detector.detect(text)