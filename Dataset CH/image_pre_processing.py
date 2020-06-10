# import the necessary packages
import cv2
import imutils
from imageai.Detection import ObjectDetection
import os

https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
def isBlurred(img, threshold):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    variance=cv2.Laplacian(gray, cv2.CV_64F).var()
    print(variance)
    if variance < threshold:
        return True
    return False


#https://github.com/imneonizer/How-to-find-if-an-image-is-bright-or-dark/blob/master/calculate_brightness.py
def isDark(img,threshold):
    img = imutils.resize(img, width=900)
    img_dot = img
   # -----Converting image to LAB Color model-----------------------------------
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)

    # -----Finding average lightness level in image by fixing some points--------
    y, x, z = img.shape  # height, width of image
    #print('>> Image Dimension => X:{}, Y:{}'.format(x, y))
    # Now we will decide some dynamic points on image for checking light intensity
    l_blur = cv2.GaussianBlur(l, (11, 11), 5)
    maxval = []
    count_percent = 3  # percent of total image
    count_percent = count_percent / 100
    row_percent = int(count_percent * x)  # 1% of total pixels widthwise
    column_percent = int(count_percent * y)  # 1% of total pizel height wise
    for i in range(1, x - 1):
        if i % row_percent == 0:
            for j in range(1, y - 1):
                if j % column_percent == 0:
                    pix_cord = (i, j)

                    cv2.circle(img_dot, (int(i), int(j)), 5, (0, 255, 0), 2)
                    img_segment = l_blur[i:i + 3, j:j + 3]
                    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(img_segment)
                    maxval.append(maxVal)

    avg_maxval = round(sum(maxval) / len(maxval))
    #print('>> Total points: {}'.format(len(maxval)))
    #print('>> Average Brightness: {}'.format(avg_maxval))
    #if avg_maxval < 50:
    #    print('>> Image is Dark')
    #    text = 'Dark'
    #else:
    #    print('>> Image is Bright')
    #    text = 'Bright'
    print(avg_maxval)
    if avg_maxval < threshold:
        return True
    return False

#https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606
def hasVehicles(image_name):
    vehicle = {"car", "truck", "bus", "train"}
    execution_path = os.getcwd()
    print(execution_path)
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(execution_path, "resnet50_coco_best_v2.0.1.h5"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , image_name),

                                              output_image_path=os.path.join(execution_path , "imagenew.jpg"))
    count_vehicle=0
    for eachObject in detections:
        print(eachObject["name"], " : ", eachObject["percentage_probability"])
        if eachObject["name"] in {"car", "truck", "bus", "train"} and eachObject["percentage_probability"]>60.0:
            count_vehicle+=1
    if  count_vehicle >3:
        return True
    return False
