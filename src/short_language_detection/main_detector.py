import re
import unicodedata

import emoji

from .detector import AbstractDetector
from .dict_detector import DictDetector
from .fasttext_detector import FastTextDetector


class Detector(AbstractDetector):
    """Main class to detect the language of a text."""

    FASTTEXT_WEIGHTS = ["lid.176.ftz", "discord_langdetect.ftz"]

    def __init__(self, reliability_threshold: float = 0.5):
        """Initializes the Detector object.

        Args:
            reliability_threshold (float, optional): The threshold above which the language is considered reliable. Defaults to 0.5.
        """
        self._reliability_threshold = reliability_threshold

        self._detectors = []
        self._detectors.append(DictDetector())

        for i, weight in enumerate(self.FASTTEXT_WEIGHTS):
            # The first detector has a weight of 1, the others have a weight of 0.5
            importance = 1 if i == 0 else 0.5

            self._detectors.append(
                FastTextDetector(weight, weighted_reliability=importance)
            )

    def _clean_text(self, text: str) -> str:
        """Cleans the text by removing special characters, emojis, and numbers.

        Args:
            text (str): The text to clean.

        Returns:
            str: The cleaned text.
        """
        text = re.sub(
            r"[!\"#$%&\'()*+,\-.\/:;<=>?@\[\\\]^_`{|}~ ]{2,}",
            lambda match: match.group()[0] + (" " if " " in match.group() else ""),
            text,
        )
        text = re.sub(r"(\w)\1{2,}", r"\1\1", text)
        text = re.sub(r"\d+|\^", "", text)

        s = "@#$<>[]*_-~&%+/§{}=\|:▬"
        for char in text:
            if char in s:
                text = text.replace(char, "", 1)

        text = emoji.replace_emoji(text, replace="").strip()

        return unicodedata.normalize("NFKC", text.replace("\n", ""))[:200]

    def detect(self, text):
        text = self._clean_text(text)
        print(text)
        predictions = [detector.detect(text) for detector in self._detectors]
        return predictions

    @property
    def supported_languages(self):
        supported_languages = set()
        for detector in self._detectors:
            supported_languages.update(detector.supported_languages)

        return list(supported_languages)
