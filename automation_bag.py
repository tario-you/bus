'''
https://map.baidu.com/dir/%E5%BE%A1%E7%BF%A0%E8%B1%AA%E5%BA%AD/%E5%87%8C%E7%99%BD%E8%B7%AF1600%E5%8F%B7/@13527856.533338789,3635804.8449999997,12.98z/maplayer%3Dtrafficforecast?querytype=nav&c=289&sn=0$$79cceb366ec94df71e5800d1$$13515199.06,3636709.88$$%E5%BE%A1%E7%BF%A0%E8%B1%AA%E5%BA%AD$$0$$$$&en=1$$$$13554160.08,3641668.53$$%E5%87%8C%E7%99%BD%E8%B7%AF1600%E5%8F%B7$$0$$$$&sc=289&ec=289&pn=0&rn=5&mrs=1&version=4&route_traffic=1&sy=0&da_src=shareurl
'''

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
            np.array(q_img), "slot.png", 0.8)
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
            np.array(q_img), "dir.png", 0.8)
        if x != -1:
            pyautogui.click(start_x+x/2+1, start_y+y/2+1)

        t(.2)

        start_x, start_y = (113, 145)

        q_img = sct.grab(
            {'mon': 1, 'top': start_y, 'left': start_x, 'width': 50, 'height': 50})
        q_img = Image.frombytes(
            "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
        x, y = find_template_coordinates(
            np.array(q_img), "car.png", 0.8)
        if x != -1:
            pyautogui.click(start_x+x/2+1, start_y+y/2+1)

        t(.2)

    pyautogui.click(524, 251)


def clear_fields(n):
    for _ in range(n-2):
        pyautogui.click(335, 245)
        pyautogui.click(335, 245)
        t(.3)
    pyautogui.click(314, 203)
    pyautogui.click(314, 245)
    t(.3)
    pyautogui.click(314, 203)
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
    # if template_path == 'rec.png':
    #     cv2.imshow("Image with Squares", img_copy)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    #     t(30)

    # Find the coordinates with the lowest y value
    min_index = np.argmin(locations[0])
    y, x = locations[0][min_index], locations[1][min_index]

    return x, y


def turn_to_list(s, last_stop):

    def add_lists(list1, list2):
        order = ['小时', '分钟', '公里', '个红绿灯']
        result = []
        groups = {}

        for item in list1 + list2:
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

    with open('automated_des.json', 'r') as f:
        data = json.load(f)

    result = add_lists(result, data['dis2school'][last_stop])

    return result


def bag_loop(data, doReload=True, record_data=True, screenshots=False):
    pyautogui.click(335, 281)  # focus onto GC

    d = {"dis2school": {}}

    sx, sy = (130, 240)
    img_start_x, img_start_y = (240, 260)
    q_start_x, q_start_y = (20, 260)

    end = "合庆镇凌白路1600号"

    reenter_data = True

    for bag_num in tqdm(range(len(data))):  # range len(data)

        if bag_num % 5 == 1:
            reload(doReload)

        if exit_program:
            sys.exit()

        bag = data[bag_num]
        d['dis2school'][f'bag{bag_num}'] = []
        for stops in bag:
            start = datetime.datetime.now()
            if reenter_data:
                clear_fields(7)  # 2
                add_fields(len(stops))

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
                    t(0.5)

                    if clicked == len(stops):
                        break

                    q_img = sct.grab(
                        {'mon': 1, 'top': q_start_y, 'left': q_start_x, 'width': 100, 'height': 722})
                    q_img = Image.frombytes(
                        "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
                    x, y = find_template_coordinates(
                        np.array(q_img), "rec.png", 0.8)
                    if x != -1:
                        break

                q_img = sct.grab(
                    {'mon': 1, 'top': q_start_y, 'left': q_start_x, 'width': 100, 'height': 722})
                q_img = Image.frombytes(
                    "RGB", q_img.size, q_img.bgra, "raw", "BGRX")
                x, y = find_template_coordinates(
                    np.array(q_img), "rec.png", 0.8)
                if x != -1:
                    pyautogui.moveTo(q_start_x+x/2+18,
                                     q_start_y+y/2+38)
                    t(0.1)
                    pyautogui.mouseDown(button='left')
                    t(0.05)
                    pyautogui.move(300, 0)
                    t(0.05)
                    pyautogui.mouseUp(button='left')
                    t(0.05)
                    pyautogui.hotkey('command', 'c')
                    t(0.3)

                    # d['dis2school'][start] = turn_to_list(pyperclip.paste())

                    d['dis2school'][f'bag{bag_num}'].append(turn_to_list(
                        pyperclip.paste(), stops[-1]))
                    with open('automated_bag.json', 'w') as f:
                        f.write(json.dumps(d, indent=4, ensure_ascii=False))

                if screenshots:
                    q_img = sct.grab(
                        {'mon': 1, 'top': 123, 'left': 0, 'width': 753, 'height': 850})
                    cv2.imwrite(
                        f'/Users/tarioyou/mwahahahh2/imgs/img{bag.index(stops)}.png', np.array(q_img))

            end = datetime.datetime.now()
            elapsed_time = end - start
            print(
                f'time elapsed for bag in stops is {elapsed_time.total_seconds()}')

            t(0.5)
        if record_data:
            with open('automated_bag.json', 'w') as f:
                f.write(json.dumps(d, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    with open('combs_output_ascii.json', 'r') as f:
        data = json.load(f)

    bag_loop(data)
