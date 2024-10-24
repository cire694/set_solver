import cv2 as cv
from label_cards import find_sets

cv.imshow("sets:", find_sets(cv.imread('../misc/set4.jpg')))
cv.waitKey(0)
cv.destroyAllWindows()