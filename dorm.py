import time
import cv2
import lib.ats
import random
import numpy as np


# get the locations of the aims
def base(sh):
    img = cv2.imread(sh, 0)
    template1 = cv2.imread('res/dorm_loc1.jpg', 0)
    template2 = cv2.imread('res/dorm_loc2.jpg', 0)
    template3 = cv2.imread('res/dorm_loc3.jpg', 0)

    res1 = cv2.matchTemplate(img, template1, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(img, template2, cv2.TM_CCOEFF_NORMED)
    res3 = cv2.matchTemplate(img, template3, cv2.TM_CCOEFF_NORMED)
    threshold = 0.75
    pos1 = []
    pos2 = []
    pos3 = []

    loc1 = np.where(res1 >= threshold)
    for pt1 in zip(*loc1[::-1]):
        pos1.append(pt1)

    loc2 = np.where(res2 >= threshold)
    for pt2 in zip(*loc2[::-1]):
        pos2.append(pt2)

    loc3 = np.where(res3 >= threshold)
    for pt3 in zip(*loc3[::-1]):
        pos3.append(pt3)

    tapX = (pos1[0][0] + pos2[0][0] + pos3[0][0]) / 3
    tapY = (pos1[0][1] + pos2[0][1] + pos3[0][1]) / 3

    tap_loc = [tapX, tapY]  # the middle of frame

    return tap_loc


# get random tap range
def tap_range(org_loc):
    orgX = org_loc[0]
    orgY = org_loc[1]

    tapX = orgX + random.uniform(-100, 600)
    tapY = orgY + random.uniform(-300, 300)

    tap_loc = [tapX, tapY]  # the final location which will be tapped

    return tap_loc


# get the "challenge" button's location
def start(sh):
    img = cv2.imread(sh, 0)
    template = cv2.imread('res/start.jpg', 0)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    pos = []

    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        pos.append(pt)

    lib.ats.tap(pos[0][0], pos[0][1])  # tap the "challenge" button


# when won
def win(sh):
    img = cv2.imread(sh, 0)
    template = cv2.imread('res/win.jpg', 0)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.75

    if (res >= threshold).any():
        return 1


# when lost
def lose(sh):
    img = cv2.imread(sh, 0)
    template = cv2.imread('res/lose.jpg', 0)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.75

    if (res >= threshold).any():
        return 1


# when tapped to a wrong place
def special(sh):
    img = cv2.imread(sh, 0)
    template = cv2.imread('res/special.jpg', 0)

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6

    if (res >= threshold).any():
        lib.ats.tap(100, 100)
        return 1


# the main method
def main():
    p = 0
    for i in range(6):
        sh = lib.ats.screenshot()
        tap_base = base(sh)
        tap_loc = tap_range(tap_base)
        lib.ats.tap(tap_loc[0], tap_loc[1])

        while lib.ats.screenshot():
            sh = lib.ats.screenshot()
            if special(sh) == 1:
                tap_loc = tap_range(tap_base)
                lib.ats.tap(tap_loc[0], tap_loc[1])
            else:
                break

        sh = lib.ats.screenshot()
        time.sleep(random.uniform(0.5, 1.5))
        start(sh)

        while lib.ats.screenshot():
            time.sleep(1)
            x1 = random.randrange(600, 800)
            y1 = random.randrange(600, 800)
            judge = lib.ats.screenshot()
            if win(judge) == 1:
                lib.ats.tap(x1, y1)
                break
            elif lose(judge) == 1:
                lib.ats.tap(x1, y1)
                p = 1
                break

        if p == 1:
            print("Lost...")
            break
        time.sleep(5)

    print("Finished")


main()
