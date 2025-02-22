import requests
import json
# importing OpenCV, time and Pandas library
# importing datetime class from datetime library
import cv2, time, pandas
import numpy as np;
from datetime import datetime

# Assigning our static_back to None
static_back = None

# List when any moving object appear
motion_list = [ None, None ]

# Time of movement
time = []

# Initializing DataFrame, one column is start
# time and other column is end time
# df = pandas.DataFrame(columns = ["Start", "End"])

# Capturing video
video = cv2.VideoCapture(0)

# Infinite while loop to treat stack of image as video
while True:
    # Reading frame(image) from video
    check, frame = video.read()

    # Initializing motion = 0(no motion)
    motion = 0

    # Converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Converting gray scale image to GaussianBlur
    # so that change can be find easily
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # In first iteration we assign the value
    # of static_back to our first frame
    if static_back is None:
        static_back = gray
        continue

    # Difference between static background
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray)

    # If change in between static background and
    # current frame is greater than 100 it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, 100, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    # Finding contour of moving object
    cnts,_ = cv2.findContours(thresh_frame.copy(),
                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle around the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Appending status of motion
    motion_list.append(motion)

    motion_list = motion_list[-2:]
  
    # Displaying image in gray_scale
    cv2.imshow("Gray Frame", gray)

    # Displaying the difference in currentframe to
    # the staticframe(very first_frame)
    cv2.imshow("Difference Frame", diff_frame)

    # Displaying the black and white image in which if
    # intensity difference greater than 30 it will appear white
    cv2.imshow("Threshold Frame", thresh_frame)

    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)

    # Appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        start_time = datetime.now()

        time.append(start_time)
        print("Start Time of Motion: ", start_time)

        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        stime = str(start_time)

        # read the image file
        image_save = cv2.imwrite('image.png', frame)

        #read image to be converted
        image = cv2.imread('image.png', 2)
          
        ret, img = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
          
        # converting to its binary form
        bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

        img = json.dumps(str(img.tolist()))

        data = {'stime': stime, 'img':img}

        res = requests.post('http://127.0.0.1:3000/motion', json=data)
        returned_data = res.json()
        #print(returned_data)


    # Appending End time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 1:
        #return the motion[-1] to 0 value so it detects the start time again
        motion_list[-1] = 0
        
        end_time = datetime.now()
        print("End Time of Motion: ", end_time)


    key = cv2.waitKey(1)    
    
    # if q entered whole process will stop
    if key == ord('q'):
    #   # if something is movingthen it append the end time of movement
        if motion == 1:
            time.append(datetime.now())
        break


video.release()

# # Destroying all the windows
cv2.destroyAllWindows()    
    # Python program to implement
    # Webcam Motion Detector
