import numpy as np
import cv2
import heapq
import statistics
import math

def get_norm(t1 , t2):
    (xa, ya, za) = t1
    (xb, yb, zb) = t2
    return math.sqrt((xa-xb)^2 + (ya-yb)^2 + (za-zb)^2)


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
    
def popularity_quant(image, k):
    finalImage = image.copy()
    color_map = popularity(image, k)
    (m,n,_) = image.shape
        
    for i in range(m):
        for j in range(n):
            t = tuple(image[i,j])
            min_dist = 100000000.0
            for col in color_map:
                dist = get_norm(t, col)
                if min_dist > dist :
                    min_dist = dist
                    min_col = col
                    
            finalImage[i,j] = np.asarray(min_col)
    return finalImage

test_image = cv2.imread('test1.png')

img = popularity_quant(test_image, 10)
cv2.imshow('Popularity Cut image',img)
cv2.waitKey()
cv2.destroyAllWindows()

cv2.imwrite('popularity_test1.png', img)

    