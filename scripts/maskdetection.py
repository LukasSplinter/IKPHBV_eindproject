# USAGE
# python detect_mask_video.py

# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
from sys import exit


#config
startTextHeight = 20
config_screenSize = 800
config_save_ROI_folder = "./data/ROI"
config_ROI_filetype = ".png"

# list with ROIs of faces for game
faceROIS = {"Mask": [], "No Mask": []}

# clear folder of old ROIS
for ROIimage in os.listdir(config_save_ROI_folder):
	#ignore .gitkeep file
	print(ROIimage)
	if "gitkeep" in ROIimage:
		continue
	os.remove(os.path.join(config_save_ROI_folder, ROIimage))

def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="./face_detector",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("--skipsnake", type=bool, default=False)
args = vars(ap.parse_args())

# if 'skipsnake' argument is added, skip straight to snake, for testing purposes
if args["skipsnake"]:
	os.system("python " + os.getcwd() + "\\scripts\\snake.py")
	exit()


# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath =  "./face_detector/deploy.prototxt"
weightsPath =   "./face_detector/res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# bool to know wether we can end detection if user desires and continue with game
	faceFound = False

	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=config_screenSize)

	# detect faces in the frame and determine if they are wearing a
	# face mask or not
	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# loop over the detected face locations and their corresponding
	# locations
	for (box, pred) in zip(locs, preds):
		# unpack the bounding box and predictions
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred

		# determine the class label and color we'll use to draw
		# the bounding box and text
		label = "Mask" if mask > withoutMask else "No Mask"
		color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

		# include the probability in the label
		label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

		# display the label and bounding box rectangle on the output
		# frame
		cv2.putText(frame, label, (startX, startY - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

		#enter faces into ROI list
			#clear faceROI list to prevent ROIs heaping up
		faceROIS["Mask"].clear()
		faceROIS["No Mask"].clear()
			#add faces to faceROIS object sorted on masked/notmasked
		faceROIS[label.split(":")[0]].append(frame[startY:endY, startX:endX])



	if len(locs) > 0:
		cv2.putText(frame, "Press 'space' to start! | klik op 'spatie' om te beginnen!", (50, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
		faceFound = True

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	#//event Handlers//

	# if 'space' pressed AND there was at least one(1) face found, end detection, save faces in root, and start game
	if faceFound and key == ord(" "):
		#bit dry but zip() wont work in this instance // oh well
		#save images to path var 'config_save_ROI_folder'
		for ROIimage in faceROIS["Mask"]:
			print("saving ROI mask")
			ROIname = "Mask" + str(faceROIS["Mask"].index(ROIimage)) + config_ROI_filetype
			cv2.imwrite(os.path.join(config_save_ROI_folder, ROIname), ROIimage)
		for ROIimage in faceROIS["No Mask"]:
			print("saving ROI no mask: " + "No Mask" + str(faceROIS["No Mask"].index(ROIimage)) + config_ROI_filetype)
			ROIname = "No Mask" + str(faceROIS["No Mask"].index(ROIimage)) + config_ROI_filetype
			cv2.imwrite(os.path.join(config_save_ROI_folder, ROIname), ROIimage)

		#end loop
		break

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

#start pygame file
if faceFound:
	os.system("python " + os.getcwd() + "\\scripts\\snake.py")