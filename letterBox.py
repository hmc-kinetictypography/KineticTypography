import os
import sys
import cv2
import numpy as np
# import csv
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from scipy.spatial import distance




"""
    Get bounding boxes around each letter 
"""
def getBounding(imagePath, numClusters, resultName):
    ogImage = cv2.imread(imagePath)
    image = cv2.imread(imagePath)
    thresh = cv2.imread("post-Threshold.tif", 0)
    image = cv2.bitwise_and(image, image, mask = thresh)
    cv2.imwrite("maskedIm.png", image)
    height, width, channels = image.shape
    labels, clusterCenters = getPredictions(imagePath, numClusters)

    for cluster in range(numClusters):
        mask = np.zeros(image.shape[:2], np.uint8)
        xList, yList = getColor(labels, imagePath, cluster)
        for i in range(len(xList)):
            xVal = xList[i]
            yVal = yList[i]

            mask[yVal, xVal] = 255
    
        kernel = np.ones((5,5),np.uint8)
        # mask = cv2.dilate(mask, kernel, iterations = 2)
        # mask = cv2.erode(mask, kernel, iterations = 2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    

        # plt.imshow(mask, cmap = "gray") 
        # plt.show()

        _ , contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            rectList = []

            # x,y,w,h = cv2.boundingRect(cnt)

            rect = cv2.minAreaRect(cnt)
            h, w = rect[1] # get width and height of rectangle
            box = cv2.boxPoints(rect) # get vertices
            box = np.int0(box) # round to nearest integer
            rect = box.tolist() # save vertices as a python list
            
            # im = cv2.drawContours(image,[box],-1,(0,0,255),2)
            # cv2.imshow("image", im)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            if w not in range(width - 25, width + 10) and h not in range(height - 25, height + 10):
                rectList.append(rect)
                ogImage = cv2.drawContours(ogImage, [box], -1, (255,0,0), 2)

                # cv2.imshow("image", image)
                cv2.imwrite(resultName, ogImage) # Save image
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()


"""
    Does the same thing as findLines but using all coordinates
"""
def getPredictions(imagePath, numClusters):
    image = cv2.imread(imagePath)
    coordList = allCoords(image)
    
    xArray = np.array(coordList) # make it into numpy array

    kmeans = KMeans(n_clusters = numClusters).fit(xArray)

    # print(kmeans.cluster_centers_)
    # print(kmeans.labels_)
    # print(kmeans.inertia_)

    return kmeans.labels_, kmeans.cluster_centers_


"""
    Takes in an image and returns all color coordinates for each pixel in the image as a list
"""
def allCoords(image):
    height, width, channels = image.shape 

    coordList = []

    for row in range(height):
        for col in range(width):
            pixel = image[row][col]

            blueVal = pixel[0]
            greenVal = pixel[1]
            redVal = pixel[2]
            
            coords = [redVal, greenVal, blueVal]
            coordList.append(coords)

    return coordList


"""
    Takes in an array of predictions for every pixel in an image, and the image path. Then it checks if the
    prediction was yellow, and if it was, it adds it to a list of x and y coordinates of the pixel and returns this list
"""
def getColor(pixArray, imagePath, clusterNumber):
    image = cv2.imread(imagePath)
    height, width, channels = image.shape 

    xList = []
    yList = []

    # locationList = []

    # 0 = blue, 1 = white, 2 = yellow

    for row in range(height):
        for col in range(width): 
            idx = row * width + col
            if pixArray[idx] == clusterNumber: 
                xList.append(col)
                yList.append(row)

    for i in range(len(pixArray)):
        if pixArray[i] == clusterNumber:
            # JM: Changed height to width here, since the arrays are one row at a time. 
            row = i // width 
            col = i % width

            xList.append(col)
            yList.append(row)

    # print(locationList)
    return xList, yList

"""
    Subtracts image2 from image1 
    If selecting frames individually, image2 is background
"""
def frameSubtract(imageName1, imageName2):
    image1 = cv2.imread(imageName1)
    image2 = cv2.imread(imageName2)
    image1 = cv2.medianBlur(image1,5)
    image2 = cv2.medianBlur(image2,5)

    #Subtraction and display of subtracted image
    #Better than im1-im2 as it prevents values from going below 0
    image3 = cv2.subtract(image2, image1)

    # cv2.imwrite("framesub.png", image3)


    #Convert to gray and then displau
    image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite("pre-Threshold Gray", image3)
    # cv2.waitKey(0)
    cv2.imwrite("framesub.png", image3)
    #Do a laplacian transform for edge detection
    #displays and saves
    laplacian1 = cv2.Laplacian(image3,cv2.CV_64F)
    # cv2.imshow("Laplacian1", laplacian1)
    cv2.imwrite("Laplacian1.tif", laplacian1)
    cv2.waitKey(0)

    #############################
    #############################
    #### Mask
    #############################

    #Binary threshold, laplace edge detection, display, save
    ret, thresh = cv2.threshold(image3, 10, 255, cv2.THRESH_BINARY)
    ret, thresh = cv2.threshold(thresh, 1, 255, cv2.THRESH_BINARY)
    cv2.imwrite("post-Threshold.tif", thresh)
    # cv2.waitKey(0)
    
    # return thresh

    laplacian2 = cv2.Laplacian(thresh,cv2.CV_64F)
    # cv2.imshow("Laplacian2", laplacian2)
    cv2.imwrite("Laplacian2.tif", laplacian2)
    # # cv2.waitKey(0)


    #Adaptive threshold: sometimes really good, sometimes terrible, honestly, it's a toss up.
    th = cv2.adaptiveThreshold(image3, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    # cv2.imshow("Adapative threshold", th)
    cv2.imwrite("Adaptive.tif", th)
    # cv2.waitKey(0)

    #Laplacian 3, edge detection on the adaptive threshold
    laplacian3 = cv2.Laplacian(th,cv2.CV_64F)
    # cv2.imshow("Laplacian3", laplacian3)
    cv2.imwrite("Laplacian3.tif", laplacian3)

############
""" MAIN """
############

if __name__=='__main__':

    # Error Handling for Command Line Arguments
    if len(sys.argv) != 4:
        print("Usage: cart.py [image name] [number of colors] [result image name]")
        sys.exit("Please make sure to include the image filepath, number of colors, and result image name as command-line arguments")

    # Save arguments as variables
    imagePath = "./Images/" + sys.argv[1]
    colors = int(sys.argv[2])
    resultPath = "./Results/" + sys.argv[3]

    # imagePath = './movie635.jpg'
    # colors = 3
    img2 = "./Images/plainDream.png"
    img1 = "./Images/redHills.png"
    frameSubtract(img1, img2)
    # thresh = frameSubtract(img1, img2)
    
    # image = cv2.imread(img1)
    # image = cv2.bitwise_and(image, image, mask = thresh)
    # cv2.imwrite("sub.tif", thresh)
    # cv2.imwrite("masked.png", image)
    getBounding(imagePath, colors, resultPath)
