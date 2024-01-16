
import pyautogui
import json
from time import sleep as t
import pyperclip
import mss
from PIL import Image
import cv2
import numpy as np
from tqdm import tqdm
import re
from pynput import keyboard
import sys
import datetime
import pandas as pd


exit_program = False


def paste():
    pyautogui.keyDown("command")
    pyautogui.press("v")
    pyautogui.keyUp("command")


def reload(doReload):
    if doReload:
        # hard reload page
        pyautogui.keyDown("command")
        pyautogui.keyDown("shift")
        pyautogui.press("r")
        pyautogui.keyUp("shift")
        pyautogui.keyUp("command")
        t(4)
        pyautogui.click(487, 198)
        t(.2)

    # select time :)
    with mss.mss() as sct:
        pyautogui.click(468, 197)

        start_x, start_y = (450, 275)

        q_img = sct.grab(
            {'mon': 1, 'top': start_y, 'left': start_x, 'width': 200, 'height': 20})
        q_img = Image.frombytes(
            "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
        x, y = find_template_coordinates(
            np.array(q_img), "../slot.png", 0.8)
        if x != -1:
            pyautogui.click(start_x+x/2+1, start_y+y/2+1)
        pyautogui.mouseDown(button='left')
        pyautogui.moveTo(515, 280)
        pyautogui.mouseUp(button='left')

        start_x, start_y = (342, 139)

        q_img = sct.grab(
            {'mon': 1, 'top': start_y, 'left': start_x, 'width': 50, 'height': 50})
        q_img = Image.frombytes(
            "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
        x, y = find_template_coordinates(
            np.array(q_img), "../dir.png", 0.8)
        if x != -1:
            pyautogui.click(start_x+x/2+1, start_y+y/2+1)

        t(.2)

        start_x, start_y = (113, 145)

        q_img = sct.grab(
            {'mon': 1, 'top': start_y, 'left': start_x, 'width': 50, 'height': 50})
        q_img = Image.frombytes(
            "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
        x, y = find_template_coordinates(
            np.array(q_img), "../car.png", 0.8)
        if x != -1:
            pyautogui.click(start_x+x/2+1, start_y+y/2+1)

        t(.2)

    pyautogui.click(524, 251)


def clear_fields():
    pyautogui.click(314, 203)
    pyautogui.click(314, 245)


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
    # if template_path == 'rec.png':
    #     cv2.imshow("Image with Squares", img_copy)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    #     t(30)

    # Find the coordinates with the lowest y value
    min_index = np.argmin(locations[0])
    y, x = locations[0][min_index], locations[1][min_index]

    return x, y


def turn_to_list(s):

    def add_lists(list1):
        order = ['小时', '分钟', '公里', '个红绿灯']
        result = []
        groups = {}

        for item in list1:
            match = re.match(r'([\d.]+)(\D+)', item)
            if match:
                num, unit = match.groups()
                num = float(num)
                if unit not in groups:
                    groups[unit] = 0
                groups[unit] += num

        for unit in order:
            if unit in groups:
                result.append(f'{groups[unit]:.1f}{unit}')

        return result

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

    result = add_lists(result)

    return result


def bag_loop(data):
    clear_fields()
    sx, sy = (130, 240)
    img_start_x, img_start_y = (240, 260)
    q_start_x, q_start_y = (20, 260)

    table_result = []

    # for bag_num in tqdm(range(len(data))):
    for bag_num in tqdm(range(len(data))):
        if bag_num != 0:
            reload(True)
        row_result = []
        for stop2 in data:
            stops = [data[bag_num], stop2]
            if data[bag_num] == stop2:
                row_result.append(['0分钟', '0公里', '0个红绿灯'])
                continue

            clear_fields()

            # for i, x in enumerate([start, end]):
            for i, x in enumerate(stops):
                # print(x)
                pyperclip.copy(x)
                pyautogui.click(sx, sy+42*(i-1))
                # t(0.1)
                paste()

            # t(0.)

            pyautogui.press("enter")

            t(1.75)

            pyautogui.moveTo(img_start_x, img_start_y)

            with mss.mss() as sct:
                q_img = sct.grab(
                    {'mon': 1, 'top': q_start_y, 'left': q_start_x, 'width': 50, 'height': 722})
                q_img = Image.frombytes(
                    "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
                # q_img.show()
                x, y = find_template_coordinates(
                    np.array(q_img), "../question.png", 0.8)
                if x != -1:
                    pyautogui.click(q_start_x+x/2, q_start_y+y/2)
                    t(0.1)

                for i in range(15):
                    pyautogui.move(0, 48)

                    pic = sct.grab(
                        {'mon': 1, 'top': img_start_y, 'left': img_start_x, 'width': 100, 'height': 722})
                    img = Image.frombytes(
                        "RGB", pic.size, pic.bgra, "raw", "BGRX")
                    # img.show()

                    x, y = find_template_coordinates(
                        np.array(img), "../choose_template.png")

                    if x != -1:
                        pyautogui.click(img_start_x+x/2, img_start_y+y/2)
                        t(0.4)
                    t(0.5)

                    q_img = sct.grab(
                        {'mon': 1, 'top': q_start_y, 'left': q_start_x, 'width': 100, 'height': 722})
                    q_img = Image.frombytes(
                        "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
                    # q_img.show()
                    # t(30)
                    x, y = find_template_coordinates(
                        np.array(q_img), "../rec.png", 0.8)
                    if x != -1:
                        break

                t(1)

                pyautogui.click(207, 306)
                t(0.3)

                q_img = sct.grab(
                    {'mon': 1, 'top': q_start_y, 'left': q_start_x, 'width': 100, 'height': 722})
                q_img = Image.frombytes(
                    "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
                # q_img.show()
                x, y = find_template_coordinates(
                    np.array(q_img), "../rec.png", 0.8)
                if x != -1:
                    pyautogui.moveTo(q_start_x+x/2+20,
                                     q_start_y+y/2+33)
                    t(.05)
                    pyautogui.mouseDown(button='left')
                    pyautogui.move(300, 0)
                    pyautogui.mouseUp(button='left')
                    t(0.05)
                    pyautogui.hotkey('command', 'c')
                    t(0.3)

                    print(pyperclip.paste())

                    row_result.append(turn_to_list(pyperclip.paste()))
                else:
                    row_result.append(['failed', stops])

                t(0.5)
        table_result.append(row_result)
        print(row_result)
        with open('term_oct_19.txt', 'a') as f:
            f.write(str(row_result))
            f.write("\n")

    return table_result


if __name__ == "__main__":
    pyautogui.click(335, 281)  # focus onto GC

    with open('assets/school.txt', 'r') as f:
        school = f.read()

    with open('assets/stops_left.txt', 'r') as f:
        left_stops = f.read().split('\n')
        left_stops.append(school)

    with open('assets/stops_right.txt', 'r') as f:
        right_stops = f.read().split('\n')
        right_stops.append(school)

    # df = pd.DataFrame([[[0] * len(right_stops)] * len(right_stops)],
    #               index=right_stops, columns=right_stops)
    # df.to_excel('assets/test.xlsx', sheet_name='new_sheet_name')

    # with open('combs_output_ascii.json', 'r') as f:
    #     data = json.load(f)

    # result = bag_loop(left_stops)

    # for f in result:
    #     for a in f:
    #         print(a, end='->')
    #         print(''.join(a))
    result = [[''.join(a) for a in f] for f in result]

    df = pd.DataFrame(result,
                      index=left_stops, columns=left_stops)
    df.to_excel('assets/updated_left_dist_2.xlsx',
                sheet_name='new_sheet_name', encoding='ascii')
