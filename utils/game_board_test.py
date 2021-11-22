import numpy as np
import cv2
import time
import colorama

colorama.init()

cap = cv2.VideoCapture(3, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_EXPOSURE, -5)


global_centers = ([(57, 37), (128, 32), (206, 29), (287, 26), (367, 32), (446, 38), (520, 44)],
                    [(49, 92), (123, 88), (203, 86), (287, 84), (371, 89), (450, 96), (524, 100)],
                    [(42, 152), (117, 151), (200, 147), (286, 147), (374, 151), (453, 154), (528, 161)],
                    [(40, 212), (113, 212), (198, 214), (283, 212), (371, 216), (455, 218), (532, 221)],
                    [(36, 277), (112, 279), (196, 283), (285, 283), (372, 281), (453, 282), (531, 286)],
                    [(33, 341), (112, 344), (195, 348), (281, 350), (370, 351), (453, 350), (531, 349)])




mtx = np.array([[793.6108905, 0., 201.56630283],
                [0., 811.4936059, 228.46068121],
                [0., 0., 1.]])

dist = np.array([[-0.76366812, -0.9773434, 0.01325336, 0.10824405, 1.83247511]])


# It take sum of brightness of center pixel (3x3)
def take_sum_around(frame, center):
    sum = 0
    # print("center",center)
    for i in range(-1, 2):
        for j in range(-1, 2):
            sum = sum + frame[center[1] + i][center[0] + j]
    return sum


# It take sum of brightness of all centers. It return table with this sum
def check_sum(frame, centers):
    sum_tab = [[0 for x in range(7)] for x in range(6)]
    for i in range(0, 6):
        for j in range(0, 7):
            sum_tab[i][j] = take_sum_around(frame, centers[i][j])
    return sum_tab


# It set cell in an array as given color if this cell value is bigger then 1000
def set_color(tab, color):
    for i in range(0, 6):
        for j in range(0, 7):
            if (tab[i][j] != 0) and str(tab[i][j]).isdigit() == True and tab[i][j] > 1000:
                tab[i][j] = str(color)
    return tab


# It connect Red and Blue table to one final table
def connect_color_tables(blue_tab, red_tab):
    for i in range(0, 6):
        for j in range(0, 7):
            if red_tab[i][j] != 0:
                blue_tab[i][j] = red_tab[i][j]
    return blue_tab


def nothing():
    pass


if __name__ == "__main__":
    TRACK_BARS = False
    cv2.namedWindow("color_frame", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("blue_mask", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("red_mask", cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar("TB: OFF/ON", "color_frame", 0, 1, nothing)

    while True:
        ret, img = cap.read()
        img = cv2.undistort(img, mtx, dist, None, mtx)
        img = img[30:410, 40:600]
        # img = cv2.bilateralFilter(img, 9, 75, 75)
        img = cv2.GaussianBlur(img, (5, 5), 0)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Add central dots
        for i in range(0, 7):
            for j in range(0, 6):
                cv2.circle(img, global_centers[j][i], 2, (255, 255, 255), 2)

        Tb_switch = cv2.getTrackbarPos("TB: OFF/ON", "color_frame")
        if Tb_switch:
            TRACK_BARS = True
            if not SET_TRACKBARS:
                SET_TRACKBARS = False
        else:
            TRACK_BARS = False
            SET_TRACKBARS = False

        if TRACK_BARS:
            cv2.namedWindow("red_mask2", cv2.WINDOW_AUTOSIZE)

            if not SET_TRACKBARS:
                cv2.createTrackbar("lower_blue_value_h", "blue_mask", 98, 255, nothing)
                cv2.createTrackbar("lower_blue_value_s", "blue_mask", 60, 255, nothing)
                cv2.createTrackbar("lower_blue_value_v", "blue_mask", 50, 255, nothing)
                cv2.createTrackbar("upper_blue_value_h", "blue_mask", 135, 255, nothing)
                cv2.createTrackbar("upper_blue_value_s", "blue_mask", 255, 255, nothing)
                cv2.createTrackbar("upper_blue_value_v", "blue_mask", 255, 255, nothing)

                cv2.createTrackbar("lower_red1_value_h", "red_mask", 0, 255, nothing)
                cv2.createTrackbar("lower_red1_value_s", "red_mask", 75, 255, nothing)
                cv2.createTrackbar("lower_red1_value_v", "red_mask", 90, 255, nothing)
                cv2.createTrackbar("upper_red1_value_h", "red_mask", 10, 255, nothing)
                cv2.createTrackbar("upper_red1_value_s", "red_mask", 255, 255, nothing)
                cv2.createTrackbar("upper_red1_value_v", "red_mask", 255, 255, nothing)

                cv2.createTrackbar("lower_red2_value_h", "red_mask2", 140, 255, nothing)
                cv2.createTrackbar("lower_red2_value_s", "red_mask2", 100, 255, nothing)
                cv2.createTrackbar("lower_red2_value_v", "red_mask2", 100, 255, nothing)
                cv2.createTrackbar("upper_red2_value_h", "red_mask2", 190, 255, nothing)
                cv2.createTrackbar("upper_red2_value_s", "red_mask2", 255, 255, nothing)
                cv2.createTrackbar("upper_red2_value_v", "red_mask2", 255, 255, nothing)
                SET_TRACKBARS = True

        # Range for first red area (range)
        if not TRACK_BARS:
            lower_red1 = np.array([0, 75, 90])
            upper_red1 = np.array([10, 255, 255])
        else:
            lower_red1_value_h = cv2.getTrackbarPos("lower_red1_value_h", "red_mask")
            lower_red1_value_s = cv2.getTrackbarPos("lower_red1_value_s", "red_mask")
            lower_red1_value_v = cv2.getTrackbarPos("lower_red1_value_v", "red_mask")
            upper_red1_value_h = cv2.getTrackbarPos("upper_red1_value_h", "red_mask")
            upper_red1_value_s = cv2.getTrackbarPos("upper_red1_value_s", "red_mask")
            upper_red1_value_v = cv2.getTrackbarPos("upper_red1_value_v", "red_mask")
            lower_red1 = np.array([lower_red1_value_h, lower_red1_value_s, lower_red1_value_v])
            upper_red1 = np.array([upper_red1_value_h, upper_red1_value_s, upper_red1_value_v])

        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

        # Range for second red area (range)
        if not TRACK_BARS:
            lower_red2 = np.array([140, 100, 100])
            upper_red2 = np.array([190, 255, 255])
        else:
            lower_red2_value_h = cv2.getTrackbarPos("lower_red2_value_h", "red_mask2")
            lower_red2_value_s = cv2.getTrackbarPos("lower_red2_value_s", "red_mask2")
            lower_red2_value_v = cv2.getTrackbarPos("lower_red2_value_v", "red_mask2")
            upper_red2_value_h = cv2.getTrackbarPos("upper_red2_value_h", "red_mask2")
            upper_red2_value_s = cv2.getTrackbarPos("upper_red2_value_s", "red_mask2")
            upper_red2_value_v = cv2.getTrackbarPos("upper_red2_value_v", "red_mask2")
            lower_red2 = np.array([lower_red2_value_h, lower_red2_value_s, lower_red2_value_v])
            upper_red2 = np.array([upper_red2_value_h, upper_red2_value_s, upper_red2_value_v])

        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask_final = red_mask1 + red_mask2
        red_mask_final = cv2.morphologyEx(red_mask_final, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        red_mask_final = cv2.morphologyEx(red_mask_final, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

        # Range for blue
        if not TRACK_BARS:
            lower_blue = np.array([98, 60, 50])
            upper_blue = np.array([135, 255, 255])
        else:
            lower_blue_value_h = cv2.getTrackbarPos("lower_blue_value_h", "blue_mask")
            lower_blue_value_s = cv2.getTrackbarPos("lower_blue_value_s", "blue_mask")
            lower_blue_value_v = cv2.getTrackbarPos("lower_blue_value_v", "blue_mask")
            upper_blue_value_h = cv2.getTrackbarPos("upper_blue_value_h", "blue_mask")
            upper_blue_value_s = cv2.getTrackbarPos("upper_blue_value_s", "blue_mask")
            upper_blue_value_v = cv2.getTrackbarPos("upper_blue_value_v", "blue_mask")
            lower_blue = np.array([lower_blue_value_h, lower_blue_value_s, lower_blue_value_v])
            upper_blue = np.array([upper_blue_value_h, upper_blue_value_s, upper_blue_value_v])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, np.ones((23, 23), np.uint8))
        blue_mask = cv2.erode(blue_mask, np.ones((6, 6), np.uint8), iterations=1)
        blue_mask = cv2.dilate(blue_mask, np.ones((5, 5), np.uint8), iterations=2)

        if TRACK_BARS:
            print("lower_blue = np.array([{0}, {1}, {2}])".format(lower_blue_value_h, lower_blue_value_s,
                                                                  lower_blue_value_v))
            print("upper_blue = np.array([{0}, {1}, {2}])".format(upper_blue_value_h, upper_blue_value_s,
                                                                  upper_blue_value_v))
            print("lower_red1 = np.array([{0}, {1}, {2}])".format(lower_red1_value_h, lower_red1_value_s,
                                                                  lower_red1_value_v))
            print("upper_red1 = np.array([{0}, {1}, {2}])".format(upper_red1_value_h, upper_red1_value_s,
                                                                  upper_red1_value_v))
            print("lower_red2 = np.array([{0}, {2}, {2}])".format(lower_red2_value_h, lower_red2_value_s,
                                                                  lower_red2_value_v))
            print("upper_red2 = np.array([{0}, {2}, {2}])".format(upper_red2_value_h, upper_red2_value_s,
                                                                  upper_red2_value_v))

        # Creating Colors Table
        sum_tab = check_sum(blue_mask, global_centers)
        blue_color_tab = set_color(sum_tab, 'B')
        sum_tab = check_sum(red_mask_final, global_centers)
        red_color_tab = set_color(sum_tab, 'R')
        color_tab = connect_color_tables(blue_color_tab, red_color_tab)

        for i in range(0, 6):
            for j in range(0, 7):
                if color_tab[i][j] == "R":
                    print(colorama.Fore.RED, color_tab[i][j], end="|")
                elif color_tab[i][j] == "B":
                    print(colorama.Fore.BLUE, color_tab[i][j], end="|")
                else:
                    print(colorama.Fore.WHITE, color_tab[i][j], end="|")
            print()
        print(colorama.Style.RESET_ALL)
        print("-------------------")

    # Add central dots for red mask
        for i in range(0, 7):
            for j in range(0, 6):
                cv2.circle(red_mask_final, global_centers[j][i], 2, (0, 0, 0), 2)
    # Add central dots for blue mask
        for i in range(0, 7):
            for j in range(0, 6):
                cv2.circle(blue_mask, global_centers[j][i], 2, (0, 0, 0), 2)
    # Show images
        cv2.imshow("color_frame", img)
        cv2.imshow("red_mask", red_mask_final)
        cv2.imshow("blue_mask", blue_mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
