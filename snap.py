from pipeline import pipeline
import cv2, sys
import matplotlib.pyplot as plt


url = sys.argv[1]
img = cv2.imread(url, 3)

plt.figure()
plt.imshow(pipeline(img))
plt.show()
