import pyautogui
import json
from time import sleep as t
import pyperclip
import mss
from PIL import Image
import cv2
import numpy as np
from tqdm import tqdm


def paste():
    pyautogui.keyDown("command")
    pyautogui.press("v")
    # t(0.1)
    pyautogui.keyUp("command")


def clear_fields(n):
    for _ in range(n-2):
        pyautogui.click(335, 245)
        t(.3)
    pyautogui.click(314, 203)
    t(.3)
    pyautogui.click(314, 245)
    t(.3)


def add_fields(n):
    for _ in range(n-2):
        pyautogui.click(335, 203)


def find_template_coordinates(img, template_path, threshold=0.7):
    # Load the template
    template = cv2.imread(template_path)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Check if the template is None
    if template is None:
        return -1, -1

    # Perform template matching
    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)

    if len(locations[0]) == 0:
        return -1, -1  # Template not found above the threshold

    # Create a copy of the image for drawing
    img_copy = img.copy()

    # Draw green-bordered squares on the copy for each location
    square_size = template.shape[:2]
    for x, y in zip(locations[1], locations[0]):
        cv2.rectangle(img_copy, (x, y),
                      (x + square_size[1], y + square_size[0]), (0, 255, 0), 2)

    # Show the image with the drawn squares
    # cv2.imshow("Image with Squares", img_copy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Find the coordinates with the lowest y value
    min_index = np.argmin(locations[0])
    y, x = locations[0][min_index], locations[1][min_index]

    return x, y


def turn_to_list(s):
    s = list(s)
    s.reverse()

    result = []
    cur = []
    for i in range(len(s)):
        cur.append(s[i])
        if i == len(s)-1 or not ((not s[i].isdigit()) or (s[i].isdigit() and (s[i+1].isdigit()) or s[i+1] == '.')) and s[i] != '.':
            cur.reverse()
            result.append(''.join(cur))
            cur = []

    result.reverse()
    return result


if __name__ == "__main__":
    pyautogui.click(335, 281)  # focus onto GC

    clear_fields(7)

    d = {"dis2school": {}}

    sx, sy = (130, 240)
    img_start_x, img_start_y = (240, 260)
    q_start_x, q_start_y = (20, 260)

    with open('combs_output_ascii.json', 'r') as f:
        data = json.load(f)

    starts = data[0][0]+data[0][1]
    end = "school"

    reenter_data = True

    mode = 1
    '''
    
    '''

    for start in starts:
        if reenter_data:
            clear_fields(2)  # 2
            add_fields(2)  # 2

            for i, x in enumerate([start, end]):
                # for i, x in enumerate(stops):
                # print(x)
                pyperclip.copy(x)
                pyautogui.click(sx, sy+42*(i-1))
                # t(0.1)
                paste()

            pyautogui.press("enter")

            t(1.5)

        pyautogui.moveTo(img_start_x, img_start_y)

        with mss.mss() as sct:
            q_img = sct.grab(
                {'mon': 1, 'top': q_start_y, 'left': q_start_x, 'width': 50, 'height': 722})
            q_img = Image.frombytes(
                "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
            # q_img.show()
            x, y = find_template_coordinates(
                np.array(q_img), "question.png", 0.8)
            if x != -1:
                pyautogui.click(q_start_x+x/2, q_start_y+y/2)
                t(0.1)

            clicked = 0

            for i in range(15):
                pyautogui.move(0, 48)

                pic = sct.grab(
                    {'mon': 1, 'top': img_start_y, 'left': img_start_x, 'width': 100, 'height': 722})
                img = Image.frombytes(
                    "RGB", pic.size, pic.bgra, "raw", "BGRX")
                # img.show()

                x, y = find_template_coordinates(
                    np.array(img), "choose_template.png")

                if x != -1:
                    pyautogui.click(img_start_x+x/2, img_start_y+y/2)
                    clicked += 1
                    t(0.4)

                if clicked == 2:
                    break

        # get time reading !!
        q_img = sct.grab(
            {'mon': 1, 'top': q_start_y, 'left': q_start_x, 'width': 100, 'height': 722})
        q_img = Image.frombytes(
            "RGB", q_img.size, q_img.bgra, "raw", "BGRX")

        x, y = find_template_coordinates(
            np.array(q_img), "rec.png", 0.8)
        if x != -1:
            pyautogui.moveTo(q_start_x+x/2+18, q_start_y+y/2+35)
            pyautogui.mouseDown(button='left')
            pyautogui.move(300, 0)
            pyautogui.mouseUp(button='left')
            t(0.1)
            pyautogui.hotkey('command', 'c')

            d['dis2school'][start] = turn_to_list(pyperclip.paste())

            with open('automated_des.json', 'w') as f:
                f.write(json.dumps(d, indent=4, ensure_ascii=False))

        t(0.2)
