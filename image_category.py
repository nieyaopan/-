import os
from PIL import Image


"""
这个是将1000张图片根据上下左右四个角的像素进行分类，因为4个角一般不会被缺口覆盖
代码中的259，115是整个图片像素size(260, 116)的顶点坐标，不能写到260、116，会报错
"""
for i in range(1000):
    image_path = "./notch_image/new_image{}.png".format(i)
    image = Image.open(image_path)
    pixel1 = image.getpixel((0, 0))
    pixel2 = image.getpixel((259, 0))
    pixel3 = image.getpixel((0, 115))
    pixel4 = image.getpixel((259, 115))
    hash_result = hash(pixel1 + pixel2 + pixel3 + pixel3)
    if not os.path.exists("./image_{}".format(hash_result)):
        os.mkdir("./image_{}".format(hash_result))
    image.save("./image_{}/{}.png".format(hash_result, i))



