from .dict_detector import DictDetector

class Detector:
    """Main class to detect the language of a text.
    """
    
    def __init__(self, reliability_threshold: float = 0.5):
        """Initializes the Detector object.

        Args:
            reliability_threshold (float, optional): The threshold above which the language is considered reliable. Defaults to 0.5.
        """
        self._reliability_threshold = reliability_threshold
        self._dict_detector = DictDetector()
        
    def predict(self, text: str) -> str:
        dict_scores = self._dict_detector.detect(text)
        return dict_scores