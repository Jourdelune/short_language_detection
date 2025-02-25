import os

import fasttext

from .detector import AbstractDetector

fasttext.FastText.eprint = lambda x: None


class FastTextDetector(AbstractDetector):
    """A language detector based on FastText"""

    WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "weights")

    def __init__(
        self,
        weight: str,
        minimum_reliability: float = 0.35,
        weighted_reliability: float = 1.0,
    ) -> None:
        """Load the FastText model"""
        self._model = fasttext.load_model(os.path.join(self.WEIGHTS_PATH, weight))
        self._minimum_reliability = minimum_reliability
        self._weighted_reliability = weighted_reliability

    def detect(self, text):
        preds = self._model.predict(text.lower(), k=5)

        # Filter out predictions with a reliability below the threshold
        predictions = []
        for i in range(len(preds[0])):
            if preds[1][i] > self._minimum_reliability:
                predictions.append(
                    (
                        preds[0][i][9:],  # Remove the "__label__" prefix
                        round(preds[1][i] * self._weighted_reliability, 2),
                    )
                )

        return predictions

    @property
    def supported_languages(self):
        return [
            label[9:] for label in self._model.get_labels()
        ]  # Remove the "__label__" prefix
