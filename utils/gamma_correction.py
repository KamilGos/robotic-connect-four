import cv2
import numpy as np


def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


mtx = np.array([[793.6108905, 0., 201.56630283],
                [0., 811.4936059, 228.46068121],
                [0., 0., 1.]])

dist = np.array([[-0.76366812, -0.9773434, 0.01325336, 0.10824405, 1.83247511]])

cap = cv2.VideoCapture(0)
if cap.isOpened() == True:
    print("OK")


while True:
    ret, main_img = cap.read()
    main_img = cv2.undistort(main_img, mtx, dist, None, mtx)
    main_img = main_img[30:410, 40:600]
    img = np.copy(main_img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    splited = list(cv2.split(img))
    splited[0] = cv2.equalizeHist(splited[0])
    # splited[0] = cv2.GaussianBlur(splited[0], (5, 5), 0)
    cv2.normalize(splited[0], splited[0], 0, 200, cv2.NORM_MINMAX)
    img = cv2.merge(splited)
    img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)

    img = adjust_gamma(img, gamma=1.5)

    cv2.imshow("Main", main_img)
    cv2.imshow("Corrected", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()