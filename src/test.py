import short_language_detection as sld

predictor = sld.Detector()
print(predictor.predict("Hi, how are you?"))