import json
import os 
import unicodedata

class DictDetector:
    """
    A language detector based on dictionaries
    """
    
    DATA_PATH = os.path.join(os.path.dirname(__file__),'data')
    
    def __init__(self) -> None:
        """
        Load the language dictionaries and the top languages
        """
        
        self._language = {}
   
        for f in os.listdir(os.path.join(self.DATA_PATH, 'dictionaries')):
            file = open(os.path.join(self.DATA_PATH, 'dictionaries', f), 'r', encoding='utf-8')
            self._language[f.split('.')[0]] = set(file.read().split('\n')) # using set for faster lookup

        self._top_languages = json.load(open(os.path.join(self.DATA_PATH, 'top_languages.json'), 'r'))
        
        # sort the top languages by popularity
        self._top_languages = [lang for lang, _ in sorted(self._top_languages.items(), key=lambda x: x[1], reverse=True)]
     
    def detect(self, string: str) -> list:
        """Detect the language of a string

        Args:
            string (str): The string to detect

        Returns:
            list: A list of tuples containing the language and the score
        """
        
        # convert the string to ascii
        string = unicodedata.normalize('NFKD', string)
 
        # remove punctuation and digits
        string = ''.join([c for c in string if c.isalpha() or c.isspace()])
        
        # split the string into words, can't use nltk because at this point we don't have know the language
        string = string.lower().split() 
        
        scores = {}

        # calculate the score for each language
        # the score is the number of common words between the string and the language dictionary
        for lang in self._language.keys():
            common_words = 0
            for v in string:
                if v in self._language[lang]:
                    common_words += 1
            scores[lang] = common_words
        
        # remove languages with score 0
        result = [(lang, scores[lang]/len(string)) for lang in scores if scores[lang] != 0]
        
        # sort the result by score
        result = sorted(result, key=lambda x: x[1], reverse=True)
        
        # sort equal scores by the top languages
        # [('fr', 1.0), ('ro', 0.5), ('en', 0.5), ('ca', 0.25), ('es', 0.25)]
        # becomes
        # [('fr', 1.0), ('en', 0.5), ('ro', 0.5), ('es', 0.25), ('ca', 0.25)]
        
        result = sorted(result, key=lambda x: (x[1], -self._top_languages.index(x[0]) if x[0] 
                                               in self._top_languages else -len(self._top_languages)), reverse=True)
        return result
