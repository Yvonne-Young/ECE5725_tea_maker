#-------------------------------------------------------------------------------
# Name:        main.py
# Purpose:     lab code
#
# Author:      Yifan Yang & Jiachen Lian
# Team ID:     yy887_jl3945
#
# Created:     12/15/2019
# Lab Section:   Monday
# Course:     Design with Embedded Operating System(ECE5725)
#------------------------------------------------------------------------------

from multiprocessing import Process,Lock,Queue
import os
import cv2 as cv
import numpy as np
import subprocess
import RPi.GPIO as GPIO
import time
import pigpio
import wavePWM

cup1 = 0
cup2 = 0

def pot_rotate():

    p2_hw = pigpio.pi()
    if not p2_hw.connected:
       exit(0)

    pwm2 = wavePWM.PWM(p2_hw) # Use default frequency
    pwm2.set_frequency(50)
    pos = 0
    pwm2.set_pulse_start_in_micros(21, pos)
    for i in range(2500, 2000, -1):
        if(i == 2004):
            pwm2.set_pulse_length_in_micros(21, 2500)
            pwm2.update()
            break
        pwm2.set_pulse_length_in_micros(21, i)
        pwm2.update()
    print('b')

def camera(q, flag, curtime, count):

    global cup1
    global cup2
    cap = cv.VideoCapture(0)
    while(True):
        if((int)(time.time()) - curtime > 25):
            flag = True

        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        img = gray
        img2 = img.copy()

        template = cv.imread('mycup.jpg',0)
        w, h = template.shape[::-1]
        meth = 'cv.TM_CCOEFF_NORMED'

        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        threshold = 0.60
        loc = np.where( res >= threshold)
        cent_x = 0
        cent_y = 0
        for pt in zip(*loc[::-1]):
            cv.rectangle(img, pt, (pt[0] + w, pt[1] + h), 255, 1)
            if pt[0] > cent_x:
                cent_x = pt[0]
                cent_y = pt[1]

        print(cent_x)
        if(cent_x >= 300 and cent_x <= 340):
          print('d')
          if(flag):
            q.put(cent_x)
            flag = False
            print(flag)
            print("####")

            curtime = (int)(time.time())
        cv.imshow('frame',img)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

def servo(q,lock,flag,curtime,count):
    global cup1
    global cup2
    p1_hw = pigpio.pi()

    if not p1_hw.connected:
       exit(0)

    pwm = wavePWM.PWM(p1_hw) # Use default frequency

    pwm.set_frequency(50)
    pos = 0
    pwm.set_pulse_start_in_micros(16, pos)
    pwm.set_pulse_length_in_micros(21, 0)
    pwm.update()

    for i in range(2500, 500, -6):

        pwm.set_pulse_length_in_micros(16, i)
        pwm.update()
        time.sleep(0.1)
        if q.empty():
            pwm.set_pulse_length_in_micros(16, i - 40)
            pwm.update()
            continue
        m = q.get()
        print(m)
        print('c')

        lock.acquire()

        pwm.set_pulse_start_in_micros(21, 0)

        j = 2500
        jj = 2100 - 50 * count
        count += 1

        while(j >= jj):
            pwm.set_pulse_length_in_micros(21, j)
            pwm.set_pulse_length_in_micros(16, 0)
            pwm.update()
            j = j - 1
        while (j <= 2500):
            pwm.set_pulse_length_in_micros(21, j)
            pwm.set_pulse_length_in_micros(16, 0)
            pwm.update()
            j = j + 1
            time.sleep(0.1)

        pwm.set_pulse_length_in_micros(21, 0)
        pwm.update()
        time.sleep(1)
        print('b')
        print('a')
        i -= 40
        pwm.set_pulse_length_in_micros(16, i)
        pwm.update()
        lock.release()

    for i in range(500, 2500, 5):
        pwm.set_pulse_length_in_micros(16, i)
        pwm.update()
    p1_hw.stop()

if __name__ == '__main__':

    q = Queue(4)
    #q.put(0)
    lock = Lock()
    flag = True
    curtime = 0
    count = 0
    p2_hw = pigpio.pi()
    if not p2_hw.connected:
       exit(0)

    pwm2 = wavePWM.PWM(p2_hw) # Use default frequency
    pwm2.set_frequency(50)
    pos = 0
    pwm2.set_pulse_start_in_micros(21, pos)
    pwm2.set_pulse_length_in_micros(21, 2500)

    pwm2.update()
    time.sleep(1)
    pwm2.set_pulse_length_in_micros(16, 2500)
    pwm2.update()
    p2_hw.stop()
    time.sleep(15)
    pc = Process(target=camera, args=(q,flag,curtime,count))
    ps = Process(target=servo, args=(q,lock,flag,curtime,count))

    pc.start()
    ps.start()
    pc.join()

    ps.terminate()
