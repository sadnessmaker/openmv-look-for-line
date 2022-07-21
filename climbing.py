GRAYSCALE_THRESHOLD = (0,15)
#设置是否使用img.binary()函数进行图像分割
BINARY_VISIBLE = True # 首先执行二进制操作，以便您可以看到正在运行的线性回归...虽然可能会降低FPS。

import sensor, image, time
import json

import struct
import lcd
import time
from pyb import Servo
from pid import PID
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)#关闭自补偿
sensor.set_auto_whitebal(False)

s1 = Servo(1)
clock = time.clock()
rho_pid = PID(p=0.4, i=0)#距离
theta_pid = PID(p=0.001, i=0)#角度

Kp=2

Trun_Angle=0


while(True):
    clock.tick()
    img = sensor.snapshot().histeq()
    img.mean(2)#进行平均滤波
    img.binary([GRAYSCALE_THRESHOLD])#对图像进行黑白分割
    img.erode(1)#

    # 函数返回回归后的线段对象line，有x1(), y1(), x2(), y2(), length(), theta(), rho(), magnitude()参数。
    # x1 y1 x2 y2分别代表线段的两个顶点坐标，length是线段长度，theta是线段的角度。
    # magnitude表示线性回归的效果，它是（0，+∞）范围内的一个数字，其中0代表一个圆。如果场景线性回归的越好，这个值越大。
    line = img.get_regression([(255,255) if BINARY_VISIBLE else THRESHOLD])
    if (line):
        rho_err = abs(line.rho())-img.width()/2
        if line.theta()>90:
            theta_err = line.theta()-180
        else:
            theta_err = line.theta()
        img.draw_line(line.line(), color = 255)
        #print(rho_err,line.magnitude(),rho_err)
        if line.magnitude()>3:
            #if -40<b_err<40 and -30<t_err<30:
            rho_output = rho_pid.get_pid(rho_err,1)
            theta_output = theta_pid.get_pid(theta_err,1)
            output = rho_output+theta_output
            output=output
            Trun_Angle=Kp*(output-0)
            if(Trun_Angle>70):    Trun_Angle=70
            elif(Trun_Angle<-70): Trun_Angle=-70
            s1.angle(Trun_Angle)
            print(output)

