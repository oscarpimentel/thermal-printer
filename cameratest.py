import cv2

print('test')
cam = cv2.VideoCapture(0)
ret, image = cam.read()
cv2.imwrite('/home/pi/testimage.jpg', image)
cam.release()
cv2.destroyAllWindows()

