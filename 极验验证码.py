import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://account.geetest.com/login'
EMAIL = '*********'
PASSWORD = '*********'


def open_firefox(url, email, password):
    '''

    :param url: 极验证登录页面地址
    :param password: 密码
    :param email: 登录账号
    :return:
    '''
    browers = webdriver.Chrome()
    browers.get(url)
    wait = WebDriverWait(browers, 20)
    email_block = wait.until(EC.presence_of_element_located((By.ID, 'email')))
    password_block = wait.until((EC.presence_of_element_located((By.ID, 'password'))))
    email_block.send_keys(email)
    password_block.send_keys(password)
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
    button.click()
    return browers, wait


def identify_gap(browers, wait):
    '''

    :param browers: 浏览器对象
    :param wait: wait对象
    :return: 缺口位置x坐标
    '''
    # 定位验证码图片
    small_img = wait.until(
        EC.presence_of_element_located((By.XPATH, '//canvas[@class="geetest_canvas_bg geetest_absolute"]')))
    location = small_img.location  # 获取图片位置，及大小
    size = small_img.size
    top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
        'width']  # 确定截图位置
    time.sleep(5)
    screenshot = browers.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))

    captcha = screenshot.crop((left, top, right, bottom))
    captcha.save(r'first.png')  # 保存图片
    first = Image.open(r'first.png')
    xsize, ysize = first.size
    pool = []  # 保存符合条件的像素点的坐标信息的数据池
    pix = first.load()
    for i in range(xsize):  # 颜色识别区域
        for j in range(ysize):
            if 159 <= (pix[i, j])[0] <= 247 and 154 <= (pix[i, j])[1] <= 249 and 102 <= (pix[i, j])[2] <= 231:
                if 0 <= abs((pix[i, j])[0] - (pix[i, j])[1]) <= 10:
                    if 18 <= abs((pix[i, j])[1] - (pix[i, j])[2]) <= 117:
                        if 1.4 <= (pix[i, j])[1] / (pix[i, j])[0] + (pix[i, j])[2] / (pix[i, j])[0] <= 1.97:
                            pool.append((i, j))
    # print(pool)
    x, y = (pool[0])[0], (pool[0])[1]  # 获取第一个符合条件的像素点的位置
    captcha1 = screenshot.crop((left + x, top + y, right, top + y + 5))  # 进行截图
    captcha1.save(r'second.png')
    Pool = []  # 第二张截图根据x坐标的每一条竖线的rgb值和的数据池
    second = Image.open(r'second.png')
    Xsize, Ysize = second.size
    pix1 = second.load()
    for i in range(Xsize):
        sum = 0
        for j in range(Ysize):
            sum += (pix1[i, j])[0] + (pix1[i, j])[1] + (pix1[i, j])[1]
        Pool.append((i, sum))
    Pool = sorted(Pool, key=lambda x: x[1])  # 排序，找出rgb值得和的最低竖线的x坐标
    # print(Pool)
    return (Pool[0])[0] + x  # 返回偏移值


if __name__ == '__main__':
    browers, wait = open_firefox(url=url, email=EMAIL, password=PASSWORD)

    print(identify_gap(browers, wait))
