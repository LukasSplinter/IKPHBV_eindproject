import os

print("[INFO] Checking for mask_detector.model")
if os.path.exists("../mask_detector.model"):
    print("[INFO] mask_detector.model found")
    print("[INFO] Running maskdetection.py")
    os.system("python maskdetection.py")
else:
    print("[INFO] mask_detector.model not found;")
    print("[INFO] Checking for mask_detector.model using getcwd()")

    if os.path.exists(os.getcwd() + "\\mask_detector.model"):
        print("[INFO] mask_detector.model found")
        print("[INFO] Running maskdetection.py")
        os.system("python " + os.getcwd() + "\\scripts\\maskdetection.py")

    else:
        print("[INFO] mask_detector.model not found, running train_maskdetection.py")
        try:
            os.system("python " + os.getcwd() + "\\scripts\\train_maskdetection.py")
        except:
            print("[INFO] train_maskdetection.py did not run")
            print("[INFO] running train_maskdetection.py using hard coded path")
            os.system("python train_maskdetection.py")
