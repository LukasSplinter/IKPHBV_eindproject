# IKPHV EINDPROJECT
#### Eindproject IKPBV, herkenning mondkapje, door:

    Lukas Splinter
    Nilesh Ramcharan
    
# DATASET:

  MaskedFace-Net dataset
    
    https://github.com/cabani/MaskedFace-Net
    
  Flickr-Faces-HQ Dataset
    
    https://github.com/NVlabs/ffhq-dataset
    
   
# GEMAAKT MET BEHULP VAN:

    ['COVID-19: Face Mask Detector with OpenCV, Keras/TensorFlow, and Deep Learning' door Adrian Rosebrock](https://www.pyimagesearch.com/2020/05/04/covid-19-face-mask-detector-with-opencv-keras-tensorflow-and-deep-learning/)
    
# BESTANDEN:

  train_maskdetection.py
    
    gebruikt de dataset om een neuraal netwerk te trainen om te herkennen of een persoon een mondkapje draagt of niet, 
    output een .model met het netwerk.
    
  mask_detector.model
  
    Dit is de output van train_maskdetection.py, hierin staan de gegevens voor het neurale netwerk.

  maskdetection.py
  
    [TODO] Dit is het bestand die het neurale netwerk runt, gebruikt het .model bestand hierboven om te kijken of er op de webcam iemand is
    die een mondkapje draagt of niet.
    
   