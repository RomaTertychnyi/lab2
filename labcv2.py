import numpy as np
import cv2
import pickle
import struct
import time

cap = cv2.VideoCapture('puma.flv')

feature_params = dict(maxCorners=100,
                      qualityLevel=0.3,
                      minDistance=7,
                      blockSize=7)

lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

color = np.random.randint(0, 255, (100, 3))

ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

mask = np.zeros_like(old_frame)

cucumber = True
f = open('Baldogno.lol', 'wb')
start = time.clock()

while (cap.isOpened()):
    ret, frame = cap.read()

    if ret:

        test = frame
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        '''print(" p1 ")
        print(p1)
        print(' p0 ')
        print(p0)'''
        good_new = p1[st == 1]
        good_old = p0[st == 1]
        print(" p1 ")
        print(good_new)
        print(' p0 ')
        print(good_old)
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            mask = cv2.line(mask, (a, b), (c, d), color[i].tolist(), 2)
            frame = cv2.circle(frame, (a, b), 5, color[i].tolist(), -1)
        img = cv2.add(frame, mask)

        cv2.imshow('frame', img)

        if cucumber:
            im = frame
            l = pickle.dumps(im)
            length = struct.pack('i', len(l))
            f.write(length)
            f.write(l)


        else:
            go = pickle.dumps(good_old)
            lgo = struct.pack('i', len(go))
            f.write(lgo)
            f.write(go)
            im = good_new
            l = pickle.dumps(im)
            length = struct.pack('i', len(l))
            f.write(length)
            f.write(l)

        cucumber = not cucumber
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        old_gray = frame_gray.copy()

        p0 = good_new.reshape(-1, 1, 2)
    else:
        break

elapsed = time.clock()
elapsed = elapsed - start
print(p0.shape)
print(len(p0))
print('time: ' + str(elapsed))
f.close()
cv2.destroyAllWindows()
cap.release()