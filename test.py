import shortlanguagedetection as ShortLanguageDetection

detection = ShortLanguageDetection.Detector() # reliable_min=0.5 in arguments for less wrong detection.
print(detection.detect('text'))
# ('en', True)