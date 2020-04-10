import requests
import cv2
import numpy
import time

start_time = time.time()
for i in range(2000):

    result = requests.get("http://192.168.1.155/api/v1/device/screenshot.png")
    image = cv2.imdecode(numpy.frombuffer(result.content, dtype='uint8'), 1)
    cv2.imwrite('./image2/{}.png'.format(i), image)  # 写入图片
    print i
    # print image
    # print image.shape

end_time = time.time()
print start_time
print end_time
print end_time-start_time
