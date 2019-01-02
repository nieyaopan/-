import os
import time
from collections import Counter

from PIL import Image
from tqdm import tqdm

start_time = time.time()
image_dir_list = ["./image_228503604", "./image_514072197", "./image_1300223107", "./image_-2095274346"]
for index, image_dir in enumerate(image_dir_list):
    image_path_list = os.listdir(image_dir)[0:30]  # 切片用30张图片足够还原一张完整的图片了
    complete_image = Image.new("RGB", (260, 116))
    # 先打开30张图片保存在列表中
    image_list = [Image.open("{}/{}".format(image_dir, i)) for i in image_path_list]

    for left in tqdm(range(0, 260)):
        # 注意get以及put位子像素不能指定顶点位子（260，116），会报错
        for down in range(0, 116):
            pixels = []
            pixel_tuple = (left, down)
            for item in image_list:
                pixels.append(item.getpixel((left, down)))  # 获取位置像素
            count = Counter(pixels)  # 获取pixels列表里面每个元素出现的次数
            most_count_pixel = count.most_common(1)[0][0]  # 获取出现次数最高的元素的值
            complete_image.putpixel(pixel_tuple, most_count_pixel)  # 写入位置像素

    complete_image.save("./complete{}.png".format(index))  # 保存图片的时候按下标保存，方便读取
stop_time = time.time()
print(stop_time - start_time)
