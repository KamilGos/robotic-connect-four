import numpy as np
import cv2
import time
import colorama


class ImageProcessing:
    def __init__(self, cam_number):
        print("+++ Camera module initialization +++")
        self.cam_num = cam_number
        self.cap = None
        self.initialized = False
        self.frame = None
        self.previous_color_tab = np.zeros([6, 7])
        self.new_color_tab = np.zeros([6, 7])
        self.global_centers = ([(57, 37), (128, 32), (206, 29), (287, 26), (367, 32), (446, 38), (520, 44)],
                               [(49, 92), (123, 88), (203, 86), (287, 84), (371, 89), (450, 96), (524, 100)],
                               [(42, 152), (117, 151), (200, 147), (286, 147), (374, 151), (453, 154), (528, 161)],
                               [(40, 212), (113, 212), (198, 214), (283, 212), (371, 216), (455, 218), (532, 221)],
                               [(36, 277), (112, 279), (196, 283), (285, 283), (372, 281), (453, 282), (531, 286)],
                               [(33, 341), (112, 344), (195, 348), (281, 350), (370, 351), (453, 350), (531, 349)])
        self.mtx = np.array([[793.6108905, 0., 201.56630283],
                             [0., 811.4936059, 228.46068121],
                             [0., 0., 1.]])
        self.dist = np.array([[-0.76366812, -0.9773434, 0.01325336, 0.10824405, 1.83247511]])

        self.lower_red1 = np.array([0, 75, 90])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([140, 100, 100])
        self.upper_red2 = np.array([190, 255, 255])
        self.lower_blue = np.array([98, 60, 50])
        self.upper_blue = np.array([135, 255, 255])

    def initialize(self):
        if not self.initialized:
            self.cap = cv2.VideoCapture(self.cam_num, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                print("Initialize", "Can't open camera ")
                self.initialized = False
            else:
                self.initialized = True
                print("+++ Camera initialized +++")
                _, self.frame = self.cap.read()

    def release_camera(self):
        self.cap.release()
        self.initialized = False

    def get_frame(self):
        _, self.frame = self.cap.read()
        self.frame = cv2.undistort(self.frame, self.mtx, self.dist, None, self.mtx)
        self.frame = self.frame[30:410, 40:600]
        self.frame = cv2.GaussianBlur(self.frame, (5, 5), 0)

    def get_masks(self):
        # print("get mask")
        for i in range(0, 5):
            self.get_frame()
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        red_mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        red_mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        red_mask_final = red_mask1 + red_mask2
        red_mask_final = cv2.morphologyEx(red_mask_final, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        red_mask_final = cv2.morphologyEx(red_mask_final, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

        blue_mask = cv2.inRange(hsv, self.lower_blue, self.upper_blue)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, np.ones((23, 23), np.uint8))
        blue_mask = cv2.erode(blue_mask, np.ones((6, 6), np.uint8), iterations=1)
        blue_mask = cv2.dilate(blue_mask, np.ones((5, 5), np.uint8), iterations=2)

        return red_mask_final, blue_mask

    # It take sum of brightness of center pixel (3x3)
    def take_sum_around(self, mask, center):
        sum = 0
        # print("center",center)
        for i in range(-1, 2):
            for j in range(-1, 2):
                sum = sum + mask[center[1] + i][center[0] + j]
        return sum

    # It take sum of brightness of all centers. It return table with this sum
    def check_sum(self, mask):
        sum_tab = [[0 for x in range(7)] for x in range(6)]
        for i in range(0, 6):
            for j in range(0, 7):
                sum_tab[i][j] = self.take_sum_around(mask, self.global_centers[i][j])
        return sum_tab

    # It set cell in an array as given color if this cell value is bigger then 1000
    def set_color(self, tab, color):
        for i in range(0, 6):
            for j in range(0, 7):
                if (tab[i][j] != 0) and str(tab[i][j]).isdigit() == True and tab[i][j] > 1000:
                    tab[i][j] = str(color)
        return tab

    # It connect Red and Blue table to one final table
    def connect_color_tables(self, blue_tab, red_tab):
        for i in range(0, 6):
            for j in range(0, 7):
                if red_tab[i][j] != 0:
                    blue_tab[i][j] = red_tab[i][j]
        return blue_tab

    def create_color_table(self):
        self.previous_color_tab = self.new_color_tab
        red_mask, blue_mask = self.get_masks()
        blue_tab = self.check_sum(blue_mask)
        blue_tab = self.set_color(blue_tab, 'B')
        red_tab = self.check_sum(red_mask)
        red_tab = self.set_color(red_tab, 'R')
        self.new_color_tab = self.connect_color_tables(blue_tab, red_tab)
        # self.print_color_table(self.new_color_tab)

    def print_color_table(self, color_tab):
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

    def check_the_difference(self):
        self.create_color_table()
        for i in range(0, 6):
            for j in range(0, 7):
                if self.previous_color_tab[i][j] != self.new_color_tab[i][j]:
                    print(self.previous_color_tab[i][j], self.new_color_tab[i][j])
                    time.sleep(3)
                    self.create_color_table()
                    if self.previous_color_tab[i][j] == self.new_color_tab[i][j]:
                        print(self.previous_color_tab[i][j], self.new_color_tab[i][j])
                        return j + 1
        return False

    def wait_for_change(self):
        # print("in")
        # i=0
        change = self.check_the_difference()
        while not change:
            change = self.check_the_difference()
            # i = i+1
            # print(i)
        return change


if __name__ == "__main__":
    colorama.init()
    ImgPrc = ImageProcessing(3)
    ImgPrc.initialize()
    # print(ImgPrc.check_the_difference())
    choose = None
    while choose != 'q':
        choose = str(input("d/q: "))
        if choose == 'd':
            # print(ImgPrc.check_the_difference())
            print(ImgPrc.wait_for_change())

    ImgPrc.release_camera()
