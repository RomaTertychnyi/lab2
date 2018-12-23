import cv2
import numpy as np
import time
import pickle
import struct
import os
import time

file = 'Baldogno.lol'
f = open(file,'rb')
obj = f.read(4)
length = struct.unpack('i',obj)[0]
obj = f.read(length)
start_im = pickle.loads(obj)

h = start_im.shape[0]
w = start_im.shape[1]
flag = False
fps = 20
size = (w,h)
videoWriter = cv2.VideoWriter('puma_dec.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, size)
info = os.stat(file)
f_size = info.st_size - length - 4
print(f_size)

start = time.clock()

image_count = 1
while(f_size):
    obj = f.read(4)
    length = struct.unpack('i',obj)[0]
    obj = f.read(length)
    pic = pickle.loads(obj)
    f_size = f_size - length - 4
    print(f_size)
    if(flag):
        print('yes')
        videoWriter.write(pic)
        start_im = pic.copy()
    else:
        image = start_im
        p0 = pic

        obj = f.read(4)
        length = struct.unpack('i',obj)[0]
        obj = f.read(length)
        p1 = pickle.loads(obj)
        f_size = f_size - length - 4

        print(len(pic))
        print(pic)
        for item in range(len(pic)):
            if int(p0[item][1])>=len(pic): continue
            if int(p0[item][0])>=len(pic): continue
            image[int(p0[item][1])][int(p0[item][0])] = start_im[int(p1[item][1])][int(p1[item][0])]
        if(image_count == 50):
            cv2.imwrite('puma_ap.jpg',image)
        print('count',image_count)
        image_count = image_count + 1

        print('no')
        videoWriter.write(image)
    flag = not flag
elapsed = time.clock()
elapsed = elapsed - start

print('time: '+ str(elapsed))
f.close()
cv2.destroyAllWindows()