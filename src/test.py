import short_language_detection as sld

predictor = sld.Detector()
print(predictor.predict("Hello, world!"))