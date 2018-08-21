import numpy as np
import cv2
import heapq
import statistics
import math

def popularity(image,k):
        (m,n,_) = image.shape
        d = {}
        for i in range(m):
            for j in range(n):
                t = tuple(image[i,j])
                if t in d:
                    d[t] += 1
                else:
                    d[t] = 1
        top_k_colors =heapq.nlargest(k, d, key=d.get)
        return top_k_colors

def get_norm(t1 , t2):
    (xa, ya, za) = t1
    (xb, yb, zb) = t2
    return math.sqrt((xa-xb)^2 + (ya-yb)^2 + (za-zb)^2)


def get_error(t1, t2):
    (xa, ya, za) = t1
    (xb, yb, zb) = t2
    return np.asarray((xa-xb)^2 , (ya-yb)^2 , (za-zb)^2 )

def dither(image, color_map):
    # Assuming we have the color map already
    finalImage = image.copy()
    (m,n,_) = image.shape
        
    for i in range(m):
        for j in range(n):
            t = tuple(image[i,j])
            min_dist = 10000.0
            for col in color_map:
                dist = get_norm(t, col)
                if min_dist > dist :
                    min_dist = dist
                    min_col = col
                    
            finalImage[i,j] = np.asarray(min_col)
            # is the error formula correct ?
            error = get_error(t, min_col)
            if(j+1 < n):
                finalImage[i,j+1] = finalImage[i, j+1] + error*(3.0/8.0)
            if(i+1 < m):
                finalImage[i+1,j] = finalImage[i+1, j] + error*(3.0/8.0)
            if(j+1 < n and i+1 < m):
                finalImage[i+1,j+1] = finalImage[i+1, j+1] + error*(1.0/4.0)
 
    return finalImage

test_image = cv2.imread('test1.png')
img = dither(test_image, popularity(test_image, 10))

cv2.imwrite('dither_test1.png', img)