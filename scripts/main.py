import os

print(os.path.exists(os.getcwd() + "\\mask_detector.model"))
print(os.path.exists(os.getcwd() + "\\bullshit.fake"))

print("[INFO] Checking working directory")
if "eindproject" not in os.getcwd().split("\\")[-1]:
    print("[INFO] Working directory not correct! Please check that you run 'scripts/main.py' in CMD from the 'ikphbv_eindproject' directory/folder!")
    exit()
else:
    print("[INFO] Working directory correct!")

    print("[INFO] Checking for mask_detector.model")
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
            print("[INFO] Please check if the file exists in the /scripts/ directory")