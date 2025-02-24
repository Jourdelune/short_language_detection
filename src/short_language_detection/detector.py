class Detector:
    def __init__(self, reliability_threshold: float = 0.5):
        self._reliability_threshold = reliability_threshold

    def predict(self, text: str) -> str:
        return self.model.predict(text)