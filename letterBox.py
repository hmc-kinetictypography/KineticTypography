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
def getBounding(imagePath, numClusters):
    image = cv2.imread(imagePath)
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
                image = cv2.drawContours(image, [box], -1, (255,0,0), 2)

                # cv2.imshow("image", image)
                cv2.imwrite("result2.png", image) # Save image
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


############
""" MAIN """
############

if __name__=='__main__':

    # Error Handling for Command Line Arguments
    if len(sys.argv) != 3:
        print("Usage: cart.py [image filepath] [number of colors]")
        sys.exit("Please make sure to include the image filepath and number of colors as command-line arguments")

    # Save arguments as variables
    imagePath = sys.argv[1]
    colors = int(sys.argv[2])

    # imagePath = './movie635.jpg'
    # colors = 3

    getBounding(imagePath, colors)
