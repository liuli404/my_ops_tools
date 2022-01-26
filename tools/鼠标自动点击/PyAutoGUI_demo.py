import pyautogui
import time

# 获取需要定位的图片
import pyautogui

img1_pos = pyautogui.locateOnScreen('1.png')
goto1_pos = pyautogui.center(img1_pos)

# 移动鼠标
pyautogui.moveTo(goto1_pos, duration=0.5)
# 点击
pyautogui.click()

# 往下相对移动 580 单位
pyautogui.moveRel(xOffset=10, yOffset=580, duration=0.5)
# 点击
pyautogui.click()

